from dataclasses import dataclass

import peewee as pw

from samudra import schemas
from samudra.models import Lemma, Konsep, Cakupan, KataAsing, CakupanXKonsep, KataAsingXKonsep, Pengguna

mock_db = pw.SqliteDatabase(':memory:')

models = [Lemma, Konsep, Cakupan, KataAsing, Pengguna]
relational_models = [CakupanXKonsep, KataAsingXKonsep]


def bind_test_database(function: callable, *args, **kwargs) -> callable:
    """Decorator to open and close a test database connection"""

    def wrapper():
        mock_db.bind(models)
        mock_db.create_tables([*models, *relational_models])
        function(*args, **kwargs)
        mock_db.drop_tables([*models, *relational_models])
        mock_db.close()

    return wrapper
