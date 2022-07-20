import peewee as pw

from samudra.conf.database import Database


class BaseTable(pw.Model):
    id = pw.AutoField(primary_key=True)
    tarikh_masuk = pw.TimestampField()

    class Meta:
        database = Database.connection
        legacy_table_name = False
