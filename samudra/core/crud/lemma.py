from typing import List


from samudra import models
from samudra.interfaces import LemmaBuilder


def create_lemma(lemma: str, force: bool = False) -> models.Lemma:
    if force:
        return models.Lemma.create(nama=lemma)
    value, exists = models.Lemma.get_or_create(nama=lemma)
    return value


def get_lemma(nama: str) -> List[models.Lemma]:
    return LemmaBuilder(nama=nama).get_cakupan().get_kata_asing().query()


def delete_lemma(lemma: models.Lemma) -> int:
    return lemma.delete_instance(recursive=True)
