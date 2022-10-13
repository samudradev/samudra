from peewee import ForeignKeyField, TextField

from ..base import BaseAttachmentDataTable, BaseRelationshipTable
from .konsep import Konsep


class KataAsing(BaseAttachmentDataTable):
    """Foreign Word model to attach to meaning from [`Konsep`][samudra.models.core.konsep.Konsep] via [`KataAsingXKonsep`][samudra.models.core.kata_asing.KataAsingXKonsep].

    ## Field
    - `nama` (TextField): the word
        * null: False
    - `bahasa` (TextField): the language the word belongs to

    ## Attr
    - `connection_table` ([`BaseRelationshipTable`][samudra.models.base.BaseRelationshipTable]) = [`KataAsingXKonsep`][samudra.models.core.kata_asing.KataAsingXKonsep]
    """

    nama = TextField(null=False)
    bahasa = TextField(null=False)

    # DEPRECATED: Uses `cls._meta.table_name` instead
    # key = "kata_asing"


class KataAsingXKonsep(BaseRelationshipTable):
    """A many-to-many relationship between [`KataAsing`][samudra.models.core.kata_asing.KataAsing] and [`Konsep`][samudra.models.core.konsep.Konsep].

    ## Fields
    - `KataAsing` (ForeignKeyField): foreign key to [`KataAsing`][samudra.models.core.kata_asing.KataAsing].
        * field: `KataAsing.id`
        * backref: `KataAsing.konsep`
        * on delete: cascade
    - `konsep` (ForeignKeyField): foreign key to [`konsep`][samudra.models.core.konsep.Konsep].
        * field: `Konsep.id`
        * backref: `Konsep.kata_asing`
        * on delete: cascade
    """

    kata_asing = ForeignKeyField(
        KataAsing, field=KataAsing.id, backref="konsep", on_delete="cascade"
    )
    konsep = ForeignKeyField(
        Konsep, field=Konsep.id, backref="kata_asing", on_delete="cascade"
    )


KataAsing.connects_to(other=Konsep, through=KataAsingXKonsep)
