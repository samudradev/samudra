from typing import List, Optional, Any

from peewee import prefetch

from samudra import models


def create_lemma(lemma: str, safe: bool = True) -> models.Lemma:
    if safe:
        return models.Lemma.get_or_create(nama=lemma)[0]
    return models.Lemma.create(nama=lemma)


def get_lemma_minimum_info(
    where: Any, limit: Optional[int] = None
) -> List[models.Lemma]:
    stmt = models.Lemma.select(models.Lemma).where(where).limit(limit)
    to_return = prefetch(
        stmt,
        models.Konsep,
        models.CakupanXKonsep,
        models.Cakupan,
        models.KataAsingXKonsep,
        models.KataAsing,
    )
    return to_return


def get_lemma(limit: int = 10) -> List[models.Lemma]:
    return get_lemma_minimum_info(where=None, limit=limit)


def get_lemma_by_name(nama: str, limit: int = 1) -> List[models.Lemma]:
    return get_lemma_minimum_info(where=models.Lemma.nama == nama, limit=limit)


def get_lemma_by_id(lemma_id: int, limit: Optional[int] = None) -> List[models.Lemma]:
    return get_lemma_minimum_info(where=(models.Lemma.id == lemma_id), limit=limit)


def delete_lemma(lemma: models.Lemma) -> int:
    return lemma.delete_instance(recursive=True)
