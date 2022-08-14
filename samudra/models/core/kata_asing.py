from peewee import ForeignKeyField, TextField

from models.base import BaseMetadataTable, BaseConnectionTable
from .konsep import Konsep


class KataAsing(BaseMetadataTable):
    """
    Lemma bahasa asing
    """

    nama = TextField(null=False)
    bahasa = TextField(null=False)

    key = "kata_asing"


class KataAsingXKonsep(BaseConnectionTable):
    kata_asing = ForeignKeyField(
        KataAsing, field=KataAsing.id, backref="konsep", on_delete="cascade"
    )
    konsep = ForeignKeyField(
        Konsep, field=Konsep.id, backref="kata_asing", on_delete="cascade"
    )


KataAsing.connection_table = KataAsingXKonsep
