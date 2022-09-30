from typing import Dict, List

from peewee import (
    AutoField,
    TextField,
    IntegerField,
    TimestampField,
    BlobField,
    ForeignKeyField,
    ModelSelect,
    CharField,
)

from ..base import (
    BaseDataTable,
    BaseAttachmentDataTable,
    BaseRelationshipTable,
    BaseStrictDataTable,
)
from .lemma import Lemma


class GolonganKata(BaseStrictDataTable):
    """Word Class model such as nouns, verbs, etc.

    ## Fields:
    - `id` (CharField): Short Name to identify the Word Class
        * max length: 6
        * unique: True
        * null: False
    - `nama` (TextField): Full name
    - `keterangan` (TextField): Description of word class
    """

    id = CharField(max_length=6, unique=True, null=False)
    nama = TextField(null=False)
    keterangan = TextField(null=False)

    def __repr__(self):
        return f"<models.GolonganKata id={self.id} nama='{self.nama}' keterangan='{self.keterangan}'>"


class Konsep(BaseDataTable):
    """Concept model to list the meanings of words from [`Lemma`][samudra.models.core.lemma.Lemma].

    ## Fields
    - `lemma` (ForeignKeyField): foreign key to [`Lemma`][samudra.models.core.lemma.Lemma].
        * field: `Lemma.id`
        * backref: `Lemma.konsep`
        * on delete: "cascade"
    - `golongan` (ForeignKeyField): foreign key to [`GolonganKata`][samudra.models.core.konsep.GolonganKata].
        * field: `GolonganKata.id`
        * backref: `GolonganKata.konsep`
        * on delete: set null
        * null: True
    - `keterangan` (TextField): the description of meaning.
        * null: True
        * index: True
    - `tertib` (IntegerField): the order in list of meaning to corresponding [`Lemma`][samudra.models.core.lemma.Lemma]
        * null: True
    """

    lemma = ForeignKeyField(
        model=Lemma, field=Lemma.id, backref="konsep", on_delete="cascade"
    )
    # TODO: Create composite key of id and tertib
    golongan = ForeignKeyField(
        model=GolonganKata, field=GolonganKata.id, on_delete="set null", null=True
    )
    keterangan = TextField(null=True, index=True)
    # ---
    tertib = IntegerField(null=True)

    def __repr__(self):
        return f"<model.{self.__class__.__name__}: id={self.id} lemma={self.lemma} golongan={self.golongan} keterangan='{self.keterangan}'>"

    def attach(
        self, to_model: BaseAttachmentDataTable, values: List[Dict[str, str]]
    ) -> ModelSelect:
        """Get or Create attachment from self to `to_model` with the corresponding `values`.

        Args:
            to_model (BaseAttachmentDataTable): Attachment data table associated with the value.
            values (List[Dict[str, str]]): Values to attach to `to_model`.

        Returns:
            pw.ModelSelect: List of attachment data associated with self.
        """
        return to_model.__attach__(self, values=values)
