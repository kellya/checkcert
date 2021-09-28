import ssl
import sys
import click
import M2Crypto


@click.command()
@click.option("--san", is_flag=True, help="Output Subject Alternate Names")
@click.option(
    "--port", default=443, type=int, help="TCP port to connect to (default 443)"
)
@click.option("--expires", is_flag=True, help="Display the expiration date")
@click.argument("domain")
def main(san, port, expires, domain):
    # handle a domain given with a : in it to specify the port
    if ":" in domain:
        uri = domain.split(":")
        domain = uri[0]
        port = uri[1]
    cert = ssl.get_server_certificate((domain, port))
    x509 = M2Crypto.X509.load_cert_string(cert)
    if san:
        all_sans = x509.get_ext("subjectAltName").get_value()
        sans = all_sans.split(",")
        for san in sans:
            print(str(san).strip().removeprefix("DNS:"))
        print(x509.get_subject().as_text())
    print(f"Certificate for {domain}\nexpires after: {x509.get_not_after()}")


if __name__ == "__main__":
    main()
