from typer import Typer
from samudra.cli import database

app = Typer()
app.add_typer(database.app, name="db")

if __name__ == "__main__":
    app()
