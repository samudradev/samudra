from typing import Optional

from ..models import Lemma


def add_lemma(nama: str, golongan: str, konsep: Optional[str] = None) -> Lemma:
    """
    Create a row in the lemma column
    :param nama: the word itself
    :param golongan: part of speech
    :param konsep: the meaning
    :return: <database.models.Lemma>
    """
    return Lemma.create(nama=nama, golongan=golongan, konsep=konsep)
