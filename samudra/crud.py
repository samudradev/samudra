from typing import List
from . import models
from . import schemas


def get_lemma(nama: str) -> models.Lemma:
    return models.Lemma.filter(models.Lemma.nama == nama).first()


def get_lemma_by_id(lemma_id: str) -> models.Lemma:
    return models.Lemma.filter(models.Lemma.id == lemma_id).first()


def create_lemma(lemma: schemas.LemmaCreation) -> models.Lemma:
    new_lemma: models.Lemma = models.Lemma(**lemma.dict())
    new_lemma.save()
    return new_lemma


def get_all_lemma() -> List[models.Lemma]:
    return [*models.Lemma.select()]
