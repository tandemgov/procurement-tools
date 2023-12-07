import json
from procurement_tools import USASpending, get_entity
import typer
from typing_extensions import Annotated

app = typer.Typer()


@app.command()
def sam(uei: str):
    """Get a SAM entity's JSON data by providing a UEI"""
    res = get_entity({"ueiSAM": uei})
    print(res.model_dump_json())


@app.command()
def usaspending(
    uei: str,
    awards: Annotated[
        bool,
        typer.Option(
            help="Get the latest awards for entity. If false, then gets the entity's profile data"
        ),
    ] = False,
):
    """Get JSON data about an entity from USASpending by providing a UEI"""

    if awards:
        res = USASpending.get_latest_recipient_awards(uei)
        print(json.dumps(res, indent=2))
    else:
        res = USASpending.get_recipient_profile(uei)
        print(json.dumps(res, indent=2))


typer_click_object = typer.main.get_command(app)
