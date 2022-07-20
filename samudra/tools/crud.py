from typing import List, Optional, Any, Union
from samudra import models
from samudra import schemas


def get_minimum_lemma_info(where: Any, limit: Optional[int] = None) -> List[models.Lemma]:
    # ? NOT FOUND? WALAUPUN ADA DALAM DATABASE
    if limit == 1:
        to_return = [models.Lemma.select(models.Lemma, models.Konsep).where(where).join(models.Konsep).limit(limit)]
    else:
        to_return = [*models.Lemma.select(models.Lemma, models.Konsep).where(where).join(models.Konsep).limit(limit)]
    return to_return


def get_lemma_by_name(nama: str, limit: int = 1) -> List[models.Lemma]:
    return get_minimum_lemma_info(where=models.Lemma.nama == nama, limit=limit)


def get_lemma_by_id(lemma_id: int, limit: int = 1) -> List[models.Lemma]:
    return get_minimum_lemma_info(where=models.Lemma.id == lemma_id, limit=limit)


def get_all_lemma(limit: int = 10) -> List[models.Lemma]:
    return get_minimum_lemma_info(where=None, limit=limit)


def create_lemma(lemma: schemas.LemmaCreation, attach_new_konsep: bool = True) -> models.Lemma:
    # existing_lemma = get_lemma(lemma.nama)
    # if existing_lemma:  # TODO: Fine tume exceptions
    #     if not attach_new_konsep:
    #         raise Exception(f"Lemmas '{lemma.nama}' already exist")
    #     else:
    #         new_konseps: List[schemas.KonsepCreation] = lemma.konsep
    #         for konsep in new_konseps:
    #             konsep.lemma = existing_lemma
    new_lemma: models.Lemma = models.Lemma(**lemma.dict())
    new_lemma.save()
    for konsep in lemma.konsep:
        new_konsep = models.Konsep.create(**konsep.dict(), lemma=new_lemma)
    return new_lemma
