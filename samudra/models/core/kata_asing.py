from peewee import ForeignKeyField, TextField

from ..base import BaseAttachmentDataTable, BaseRelationshipTable
from .konsep import Konsep


class KataAsing(BaseAttachmentDataTable):
    """
    Lemma bahasa asing
    """

    nama = TextField(null=False)
    bahasa = TextField(null=False)

    key = "kata_asing"


class KataAsingXKonsep(BaseRelationshipTable):
    kata_asing = ForeignKeyField(
        KataAsing, field=KataAsing.id, backref="konsep", on_delete="cascade"
    )
    konsep = ForeignKeyField(
        Konsep, field=Konsep.id, backref="kata_asing", on_delete="cascade"
    )


KataAsing.connection_table = KataAsingXKonsep
