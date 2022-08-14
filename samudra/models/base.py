from typing import List, Dict

import peewee as pw

from samudra.conf.database.core import Database
from samudra.conf.database.fields import IDField


class BaseTable(pw.Model):
    id = IDField[Database.engine]
    tarikh_masuk = pw.TimestampField()

    class Meta:
        database = Database.connection
        legacy_table_name = False


class BaseConnectionTable(BaseTable):
    pass


class BaseMetadataTable(BaseTable):
    connection_table: BaseConnectionTable

    @classmethod
    def __attach__(
        cls, other: BaseTable, values: List[Dict[str, str]]
    ) -> pw.ModelSelect:
        rows = [cls.get_or_create(**value)[0] for value in values]
        model_name = getattr(cls, "key", cls.__name__.lower())
        for row in rows:
            try:
                cls.connection_table.get_or_create(
                    **{model_name: row.id, other.__class__.__name__.lower(): other.id}
                )
            except AttributeError:
                raise AttributeError(f"{cls} has no associated connection table")
        return getattr(other, model_name)
