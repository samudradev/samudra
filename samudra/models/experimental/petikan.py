from peewee import TextField, ForeignKeyField, DateField

from samudra.models import Konsep
from samudra.models.base import (
    BaseAttachmentDataTable,
    BaseRelationshipTable,
    BaseDataTable,
)


class SumberPetikan(BaseDataTable):
    """🧪 EXPERIMENTAL Source of the sentence in [`Petikan`][samudra.models.experimental.petikan.Petikan]."""

    tajuk = TextField(null=False, index=True)
    tarikh = DateField()
    # ? Aku masih tak tahu macam mana nak uruskan metadata dari pelbagai jenis sumber
    metadata = TextField(null=True)


class Petikan(BaseAttachmentDataTable):
    """🧪 EXPERIMENTAL Sentence from sources that used the [`Lemma`][samudra.models.core.lemma.Lemma] in the sense described by [`Konsep`][samudra.models.core.konsep.Konsep]."""

    petikan = TextField(null=False, index=True)
    # --> Pautan ke SumberPetikan
    sumber = ForeignKeyField(
        model=SumberPetikan,
        field=SumberPetikan.id,
        backref="petikan",
        on_delete="set null",
        null=True,
    )


class PetikanXKonsep(BaseRelationshipTable):
    """🧪 EXPERIMENTAL A many-to-many relationship between [`Petikan`][samudra.models.experimental.petikan.Petikan] and [`Konsep`][samudra.models.core.konsep.Konsep].

    ## Fields
    - `Petikan` (ForeignKeyField): foreign key to [`Petikan`][samudra.models.experimental.petikan.Petikan].
        * field: `Petikan.id`
        * backref: `Petikan.konsep`
        * on delete: cascade
    - `konsep` (ForeignKeyField): foreign key to [`Konsep`][samudra.models.core.konsep.Konsep].
        * field: `Konsep.id`
        * backref: `Konsep.petikan`
        * on delete: cascade
    """

    petikan = ForeignKeyField(
        model=Petikan, field=Petikan.id, backref="konsep", on_delete="cascade"
    )
    konsep = ForeignKeyField(
        model=Konsep, field=Konsep.id, backref="petikan", on_delete="cascade"
    )


Petikan.connects_to(other=Konsep, through=PetikanXKonsep)
