from checkcert.checkcert import main as cert_main
from checkcert.checkcert import __version__ as cert_version
from click.testing import CliRunner

runner = CliRunner()


def test_main():
    if cert_main:
        response = runner.invoke(cert_main, ["www.franklin.edu"])
        assert response.exit_code == 0
        response = runner.invoke(cert_main, ["www.franklin.edu:443"])
        assert response.exit_code == 0


def test_version():
    response = runner.invoke(cert_main, ["--version"])
    assert response.exit_code == 0
    assert cert_version in response.output


def test_dump():
    response = runner.invoke(cert_main, ["www.franklin.edu", "--dump"])
    assert response.exit_code == 0


def test_san():
    response = runner.invoke(cert_main, ["www.franklin.edu", "--san"])
    assert response.exit_code == 0
