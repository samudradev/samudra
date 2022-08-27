from typing import List, Dict

import peewee as pw

from samudra.conf.database.core import Database


class BaseDataTable(pw.Model):
    id = pw.AutoField(primary_key=True)
    tarikh_masuk = pw.TimestampField()

    class Meta:
        database = Database.connection
        legacy_table_names = False


class BaseRelationshipTable(BaseDataTable):
    pass


class BaseAttachmentDataTable(BaseDataTable):
    connection_table: BaseRelationshipTable

    @classmethod
    def __attach__(
            cls, other: BaseDataTable, values: List[Dict[str, str]]
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


class BaseStrictDataTable(BaseDataTable):
    @classmethod
    def get_or_create(cls, **kwargs):
        raise AttributeError(
            f"{cls} is a strict table. Rows can only be created explicitly by the `Model.create` method.")