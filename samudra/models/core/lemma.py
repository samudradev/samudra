from peewee import TextField

from samudra.models.base import BaseDataTable


class Lemma(BaseDataTable):
    """Word Entry model such that listed in the dictionary.

    ## Fields
    - `nama` (TextField): the word as displayed on a dictionary.
        * null: False
    """

    nama = TextField(null=False)

    def __repr__(self) -> str:
        return f"<model.{self.__class__.__name__}: id={self.id} nama={self.nama}>"
