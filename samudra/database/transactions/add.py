from typing import Optional

from ..models import Konsep


def add_lemma(lemma: str, golongan: str, konsep: Optional[str] = None) -> Konsep:
    """
    Create a row in the lemma column
    :param lemma: the word itself
    :param golongan: part of speech
    :param konsep: the meaning
    :return: <database.models.Lemma>
    """
    return Konsep.create(lemma=lemma, golongan=golongan, konsep=konsep)
