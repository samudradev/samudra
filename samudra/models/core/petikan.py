from peewee import TextField, ForeignKeyField, DateField

from models import Konsep
from models.base import BaseAttachmentDataTable, BaseRelationshipTable, BaseDataTable


class SumberPetikan(BaseDataTable):
    tajuk = TextField(null=False, index=True)
    tarikh = DateField()
    #? Aku masih tak tahu macam mana nak uruskan metadata dari pelbagai jenis sumber
    metadata = TextField(null=True) 


class Petikan(BaseAttachmentDataTable):
    petikan = TextField(null=False, index=True)
    # --> Pautan ke SumberPetikan
    sumber = ForeignKeyField(model=SumberPetikan, field=SumberPetikan.id, backref='petikan', on_delete='set null',
                             null=True)


class PetikanXKonsep(BaseRelationshipTable):
    petikan = ForeignKeyField(model=Petikan, field=Petikan.id, backref='konsep', on_delete='cascade')
    konsep = ForeignKeyField(model=Konsep, field=Konsep.id, backref='petikan', on_delete='cascade')


Petikan.connection_table = PetikanXKonsep
