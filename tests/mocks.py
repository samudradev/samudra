import peewee as pw

from samudra import schemas
from samudra.models import Lemma, Konsep, Cakupan, KataAsing

mock_db = pw.SqliteDatabase(':memory:')

models = [Lemma, Konsep, Cakupan, KataAsing]


def bind_test_database(function: callable, *args, **kwargs) -> callable:
    """Decorator to open and close a test database connection"""

    def wrapper():
        mock_db.bind(models)
        mock_db.create_tables(models)
        function(*args, **kwargs)
        mock_db.close()

    return wrapper


def single_complete_test_lemma(cakupan: bool = True, kata_asing: bool = True) -> schemas.LemmaCreation:
    """Single boilerplate data for testing purposes"""
    return schemas.LemmaCreation(
        nama='lemma ujian',
        konsep=[
            schemas.KonsepCreation(
                keterangan='Ini adalah lemma yang digunakan untuk ujian',
                golongan='kata nama',
                cakupan=[
                    schemas.CakupanCreation(
                        nama='ujian',
                        keterangan='lemma ini tak wujud di luar ujian'
                    )
                ] if cakupan else None,
                kata_asing=[
                    schemas.KataAsingCreation(
                        nama='test lemma',
                        golongan='kata nama',
                        bahasa='en'
                    )
                ] if kata_asing else None
            )
        ]
    )
