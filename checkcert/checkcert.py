# heavily modified version of https://gist.githubusercontent.com/gdamjan/55a8b9eec6cf7b771f92021d93b87b2c/raw/d8dc194ec4d0187f985a57138019d04e3a59b51f/ssl-check.py
# to give a CLI for passing the hosts to check and other optional output
import click
from OpenSSL import SSL
from OpenSSL import crypto
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna
import sys

from socket import socket
from collections import namedtuple

__version__ = "0.1.0"

HostInfo = namedtuple(
    field_names="cert hostname peername is_valid", typename="HostInfo"
)


def get_certificate(hostname, port):
    hostname_idna = idna.encode(hostname)
    sock = socket()

    try:
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
    except ConnectionRefusedError:
        pass

    return HostInfo(
        cert=crypto_cert,
        peername=peername,
        hostname=hostname,
        is_valid=not cert.has_expired(),
    )


def get_alt_names(cert):
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return None


def get_x509_text(cert):
    return crypto.dump_certificate(crypto.FILETYPE_TEXT, cert)


def get_common_name(cert):
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None


def get_issuer(cert):
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None


def print_basic_info(hostinfo):
    print(
        f"""
{hostinfo.hostname} ({hostinfo.peername[0]}:{hostinfo.peername[1]})
\tcommonName: {get_common_name(hostinfo.cert)}
\tSAN: {get_alt_names(hostinfo.cert)}
\tissuer: {get_issuer(hostinfo.cert)}
\tnotBefore: {hostinfo.cert.not_valid_before}
\tnotAfter:  {hostinfo.cert.not_valid_after}
          """
    )


@click.command()
@click.version_option(__version__, prog_name="checkcert")
@click.option("--san", is_flag=True, help="Output Subject Alternate Names")
@click.option(
    "--dump", is_flag=True, help="Dump the full text version of the x509 certificate"
)
@click.option("--color/--no-color", default=True)
@click.argument("hosts", nargs=-1)
def main(san, dump, color, hosts):
    # setup the list of tuples
    HOSTS = []
    # handle a domain given with a : in it to specify the port
    for host in hosts:
        # if  a host has a : in it, split on the :, first field will be host
        # second field will be the port
        if ":" in host:
            host_info = host.split(":")
            HOSTS.append((host_info[0], int(host_info[1])))
        else:
            HOSTS.append((host, 443))
    for hostinfo in map(lambda x: get_certificate(x[0], x[1]), HOSTS):
        output_string = ""
        if dump:
            print(get_x509_text(hostinfo.cert).decode())
        else:
            output_string += (
                f"{hostinfo.hostname} ({hostinfo.peername[0]}:{hostinfo.peername[1]})\n"
            )
            output_string += f"\tcommonName: {get_common_name(hostinfo.cert)}\n"
            if san:
                output_string += f"\tSAN: {get_alt_names(hostinfo.cert)}\n"
            output_string += f"\tissuer: {get_issuer(hostinfo.cert)}\n"
            output_string += f"\tnotBefore: {hostinfo.cert.not_valid_before}\n"
            output_string += f"\tnotAfter:  {hostinfo.cert.not_valid_after}\n\n"
            if hostinfo.is_valid and color:
                click.echo(click.style(output_string, fg="green"))
            elif not hostinfo.is_valid and color:
                click.echo(click.style(output_string, fg="red"))
            else:
                click.echo(click.style(output_string))

    # print(f"Certificate for {domain}\nexpires after: {x509.get_not_after()}")


if __name__ == "__main__":
    main()  # pragma: no cover
