from peewee import SqliteDatabase

from samudra.models import Lemma, Konsep, Ragam, Cakupan, KataAsing

mock_db = SqliteDatabase(':memory:')

models = [Lemma, Konsep, Ragam, Cakupan, KataAsing]
