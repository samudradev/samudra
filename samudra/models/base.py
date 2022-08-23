import peewee as pw

from samudra.conf.database.core import Database
from samudra.conf.database.fields import IDField


class BaseTable(pw.Model):
    id = IDField[Database.engine]
    tarikh_masuk = pw.TimestampField()

    class Meta:
        database = Database.connection
        legacy_table_names = False
