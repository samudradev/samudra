from typing import List, Dict

import typer

from samudra.core import crud
from samudra.conf.setup import access_database
from samudra.models import bind_to_database

app = typer.Typer()


@app.command()
def new(
    lemma: str = typer.Argument(..., rich_help_panel="Word to register to database"),
    concept: str = typer.Option(
        None,
        "--concept",
        "-c",
        rich_help_panel="The concept to associate with the word.",
    ),
    golongan: str = typer.Option(
        None, "--class", "--gol", rich_help_panel="The class the concept belongs to"
    ),
    tags: List[str] = typer.Option(
        None, "--tags", "-t", rich_help_panel="The tags the concept belongs to (Multi)"
    ),
    en: List[str] = typer.Option(
        None, rich_help_panel="The english equivalent for the same concept (Multi)"
    ),
    force: bool = typer.Option(
        False, rich_help_panel="Create a new lemma not caring if it already created"
    ),
):
    bind_to_database(database=access_database(local=True), auth=True, experimental=True)
    if concept is None:
        crud.create_lemma(lemma=lemma, force=force)
    crud.create_konsep(
        lemma=lemma,
        concept=concept,
        golongan=golongan,
        tags=tags,
        foreign={"en": en},
        force_lemma=force,
    )


# TODO get
# TODO edit
# TODO delete
