from typer import Typer

from samudra.cli import database, lemma, golongan_kata

app = Typer()
app.add_typer(database.app, name="db", rich_help_panel="Interact with the database")
app.add_typer(lemma.app, name="lemma", rich_help_panel="Interact with lemmas")
app.add_typer(
    golongan_kata.app, name="class", rich_help_panel="Interact with word classes"
)

if __name__ == "__main__":
    app()
