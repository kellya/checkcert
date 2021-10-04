""" Tests to validate checkcert"""
from click.testing import CliRunner
from checkcert.checkcert import main as cert_main
from checkcert.checkcert import __version__ as cert_version

runner = CliRunner()


def test_main():
    """validate the core function returns correctly for:
    a domain
    a domain and a port
    no names specified
    a list of domains
    a list of domains with a port specified on one
    """
    response = runner.invoke(cert_main, ["www.franklin.edu"])
    assert response.exit_code == 0
    response = runner.invoke(cert_main, ["www.franklin.edu:443"])
    assert response.exit_code == 0
    response = runner.invoke(cert_main, ["www.franklin.edu", "--no-color"])
    assert response.exit_code == 0
    response = runner.invoke(cert_main, ["www.franklin.edu", "library.franklin.edu"])
    assert response.exit_code == 0
    response = runner.invoke(
        cert_main, ["www.franklin.edu:443", "library.franklin.edu"]
    )
    assert response.exit_code == 0


def test_version():
    """get the version output and ensure it matches the version var"""
    response = runner.invoke(cert_main, ["--version"])
    assert response.exit_code == 0
    assert cert_version in response.output


def test_dump():
    """verify that --dump outputs data"""
    response = runner.invoke(cert_main, ["www.franklin.edu", "--dump"])
    assert response.exit_code == 0
    assert "www.franklin.edu" in response.output


def test_san():
    """verify --san outputs correctly"""
    response = runner.invoke(cert_main, ["www.franklin.edu", "--san"])
    assert response.exit_code == 0


def test_san_only():
    """verify --san outputs correctly"""
    response = runner.invoke(cert_main, ["www.franklin.edu", "--san-only"])
    assert response.exit_code == 0


def test_bad_cert():
    """verify an expired certificate works"""
    response = runner.invoke(cert_main, ["support.bluequill.com", "--san"])
    assert response.exit_code == 0


def test_from_file():
    """Verify loading domains from file"""
    response = runner.invoke(cert_main, ["--filename", "ci/test_domains.txt"])
    assert response.exit_code == 0
