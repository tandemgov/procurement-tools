from typer.testing import CliRunner
from procurement_tools.cli.main import app

runner = CliRunner()


def test_sam(sam_api_results):
    result = runner.invoke(app, ["sam", "entity", "XRVFU3YRA2U5"])
    assert result.exit_code == 0
    assert "JAMES & ENYART" in result.stdout


def test_sam_opportunities(sam_opportunties):
    result = runner.invoke(
        app,
        [
            "sam",
            "opportunities",
            "--title",
            "SPRUCE",
            "--postedfrom",
            "12/14/2023",
            "--postedto",
            "12/14/2023",
        ],
    )
    assert result.exit_code == 0
    assert (
        "DA01--VA Secure, Performant, Reliable, and User-Centered  Experiences (SPRUCE)"
        in result.stdout
    )


def test_usaspending_recipient_profile(usas_recipient_api_results):
    result = runner.invoke(app, ["usaspending", "J7M9HPTGJ1S9"])
    assert result.exit_code == 0
    assert "TRIWEST" in result.stdout


def test_usaspending_recipient_profile(usas_awards_api_results):
    result = runner.invoke(app, ["usaspending", "J7M9HPTGJ1S9", "--awards"])
    assert result.exit_code == 0
    assert "CONT_AWD_36C10G24F0004_3600_36C10G21D0001_3600" in result.stdout


def test_sbir_get_awards(sbir_awards_api_results):
    result = runner.invoke(app, ["sbir", "awards"])
    assert result.exit_code == 0
    assert "MEDICARBONE" in result.stdout


def test_sbir_get_solicitations(sbir_solicitations_api_results):
    result = runner.invoke(app, ["sbir", "solicitations"])
    assert result.exit_code == 0
    assert "Advancing Research" in result.stdout
