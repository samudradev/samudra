import typer

from samudra.core import crud
from samudra.conf.setup import access_database
from samudra.models import bind_to_database
from samudra.schemas import CreateGolonganKata

app = typer.Typer()


@app.command()
def new(
    id: str = typer.Argument(
        ..., rich_help_panel="Identifying shorthand. Must be less than 6"
    ),
    nama: str = typer.Argument(..., rich_help_panel="Full name of the word class"),
    keterangan: str = typer.Option(
        "", "--keterangan", "-k", rich_help_panel="The description of the word class"
    ),
):
    """Creates a new word class."""
    # TODO Only bind during instantiation
    bind_to_database(database=access_database(local=True), auth=True, experimental=True)
    crud.create_golongan_kata(
        data=CreateGolonganKata(id=id, nama=nama, keterangan=keterangan)
    )
