from typing import List
from . import models
from . import schemas


def get_lemma(nama: str) -> models.Lemma:
    return models.Lemma.filter(models.Lemma.nama == nama).first()


def get_lemma_by_id(lemma_id: str) -> models.Lemma:
    return models.Lemma.filter(models.Lemma.id == lemma_id).first()


def create_lemma(lemma: schemas.LemmaCreation, attach_new_konsep: bool = True) -> models.Lemma:
    existing_lemma = get_lemma(lemma.nama)
    if existing_lemma:  # TODO: Fine tume exceptions
        if not attach_new_konsep:
            raise Exception(f"Lemmas '{lemma.nama}' already exist")
        else:
            new_konseps: List[schemas.KonsepCreation] = lemma.konsep
            for konsep in new_konseps:
                konsep.lemma = existing_lemma
    new_lemma: models.Lemma = models.Lemma(**lemma.dict())
    new_lemma.save()
    return new_lemma


def get_all_lemma() -> List[models.Lemma]:
    """Gets all lemma name"""
    return [*models.Lemma.select()]
