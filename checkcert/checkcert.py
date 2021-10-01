""" CLI to get basic information about certificates and determine validity"""
from collections import namedtuple
import concurrent.futures
from socket import socket
import click
from OpenSSL import SSL
from OpenSSL import crypto
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna


__version__ = "0.4.0"

HostInfo = namedtuple(
    field_names="cert hostname peername is_valid", typename="HostInfo"
)


def get_certificate(hostname: str, port: int) -> HostInfo:
    """retrieve certificate details and return HostInfo tuple of values"""
    hostname_idna = idna.encode(hostname)
    sock = socket()

    sock.connect((hostname, port))
    peername = sock.getpeername()
    ctx = SSL.Context(SSL.SSLv23_METHOD)  # most compatible
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE
    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_connect_state()
    sock_ssl.set_tlsext_host_name(hostname_idna)
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    crypto_cert = cert.to_cryptography()
    sock_ssl.close()
    sock.close()

    return HostInfo(
        cert=crypto_cert,
        peername=peername,
        hostname=hostname,
        is_valid=not cert.has_expired(),  # is_valid is the inverse of has_expired
    )


def get_alt_names(cert: str) -> str:
    """retrieve the SAN values for given cert"""
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:  # pragma: no cover
        return None


def get_x509_text(cert: str) -> str:
    """return the human-readable text version of the certificate"""
    return crypto.dump_certificate(crypto.FILETYPE_TEXT, cert)


def get_common_name(cert: str) -> str:
    """Return the common name from the certificate"""
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:  # pragma: no cover
        return None


def get_issuer(cert: str) -> str:
    """Return the name of the CA/Issuer of the certificate"""
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:  # pragma: no cover
        return None


def get_host_list_tuple(hosts: list) -> list:
    """create a tuple of host and port based on hosts given to us in the form
    host:port
    """
    all_hosts = []
    for host in hosts:
        # if  a host has a : in it, split on the :, first field will be host
        # second field will be the port
        if ":" in host:
            host_info = host.split(":")
            all_hosts.append((host_info[0], int(host_info[1])))
        else:
            all_hosts.append((host, 443))
    return all_hosts


@click.command()
@click.version_option(__version__, prog_name="checkcert")
@click.option("--san", is_flag=True, help="Output Subject Alternate Names")
@click.option(
    "--dump", is_flag=True, help="Dump the full text version of the x509 certificate"
)
@click.option(
    "--color/--no-color",
    default=True,
    help="Enable/disable ANSI color output to show cert validity",
)
@click.option(
    "--filename",
    "-f",
    type=click.Path(),
    help="Read a list of hosts to check from a file",
)
@click.option(
    "--valid/--no-valid", default=True, help="Show True/False for cert validity"
)
@click.argument("hosts", nargs=-1)
def main(san, dump, color, filename, valid, hosts):
    """Return information about certificates given including their validity"""
    # setup the list of tuples
    # handle a domain given with a : in it to specify the port
    if filename:
        hosts = []
        with open(filename, "r", encoding="utf-8") as infile:
            for line in infile:
                line = line.strip()
                hosts.append(line)
    all_hosts = get_host_list_tuple(hosts)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as epool:
        for hostinfo in epool.map(lambda x: get_certificate(x[0], x[1]), all_hosts):
            output_string = "\n"
            if dump:
                print(get_x509_text(hostinfo.cert).decode())
            else:
                output_string += (
                    f"{hostinfo.hostname} "
                    f"({hostinfo.peername[0]}:{hostinfo.peername[1]})\n"
                )
                output_string += f"    commonName: {get_common_name(hostinfo.cert)}\n"
                output_string += f"        issuer: {get_issuer(hostinfo.cert)}\n"
                output_string += f"     notBefore: {hostinfo.cert.not_valid_before}\n"
                output_string += f"      notAfter: {hostinfo.cert.not_valid_after}\n"
                if valid:
                    output_string += f"         Valid: {hostinfo.is_valid}\n"
                if san:
                    output_string += f"           SAN: {get_alt_names(hostinfo.cert)}\n"
                if hostinfo.is_valid and color:
                    click.echo(click.style(output_string, fg="green"))
                elif not hostinfo.is_valid and color:
                    click.echo(click.style(output_string, fg="red"))
                else:
                    click.echo(click.style(output_string))


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter # pragma: no cover
