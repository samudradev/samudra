from dataclasses import dataclass

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
