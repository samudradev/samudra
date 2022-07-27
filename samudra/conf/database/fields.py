import enum
from typing import Dict

import peewee as pw
import playhouse.cockroachdb as crdb

from samudra.conf.database.options import DatabaseEngine

IDField: Dict[DatabaseEngine, pw.Field] = {
    DatabaseEngine.SQLite: pw.AutoField(primary_key=True),
    DatabaseEngine.MySQL: pw.AutoField(primary_key=True),
    DatabaseEngine.CockroachDB: crdb.RowIDField(primary_key=True)
}
