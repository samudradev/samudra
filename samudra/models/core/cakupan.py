from peewee import BlobField, TextField, ForeignKeyField

from ..base import BaseDataTable, BaseAttachmentDataTable, BaseRelationshipTable
from .konsep import Konsep


class Cakupan(BaseAttachmentDataTable):
    """Context model to attach to meaning from [`Konsep`][samudra.models.core.konsep.Konsep] via [`CakupanXKonsep`][samudra.models.core.cakupan.CakupanXKonsep].

    ## Fields
    - `nama` (TextField): the context name
        * null: False
        * unique: True
    - `keterangan` (TextField): the description of the context
        * null: True

    ## Attrs
    - `connection_table` ([`BaseRelationshipTable`][samudra.models.base.BaseRelationshipTable]): [`CakupanXKonsep`][samudra.models.core.cakupan.CakupanXKonsep]
    """

    nama = TextField(null=False, unique=True)
    keterangan = TextField(null=True)


class CakupanXKonsep(BaseRelationshipTable):
    """A many-to-many relationship between [`Cakupan`][samudra.models.core.cakupan.Cakupan] and [`Konsep`][samudra.models.core.konsep.Konsep].

    ## Fields
    - `cakupan` (ForeignKeyField): foreign key to [`Cakupan`][samudra.models.core.cakupan.Cakupan].
        * field: `Cakupan.id`
        * backref: `Cakupan.konsep`
        * on delete: cascade
    - `konsep` (ForeignKeyField): foreign key to [`konsep`][samudra.models.core.konsep.Konsep].
        * field: `Konsep.id`
        * backref: `Konsep.cakupan`
        * on delete: cascade
    """

    cakupan = ForeignKeyField(
        model=Cakupan, field=Cakupan.id, backref="konsep", on_delete="cascade"
    )
    konsep = ForeignKeyField(
        model=Konsep, field=Konsep.id, backref="cakupan", on_delete="cascade"
    )


Cakupan.connects_to(other=Konsep, through=CakupanXKonsep)
