from typing import Any, Optional, List

from peewee import prefetch

from samudra import models


def get_kata_asing_minimum_info(
    where: Any, limit: Optional[int] = None
) -> List[models.KataAsing]:
    stmt = models.KataAsing.select(models.KataAsing).where(where).limit(limit)
    to_return = prefetch(stmt, models.KataAsingXKonsep, models.Konsep, models.Lemma)
    return to_return


def get_kata_asing(limit: int = 10) -> List[models.KataAsing]:
    return get_kata_asing_minimum_info(where=None, limit=limit)


def get_kata_asing_by_name(nama: str, limit: int = 1) -> List[models.KataAsing]:
    return get_kata_asing_minimum_info(where=models.KataAsing.nama == nama, limit=limit)


def get_kata_asing_by_id(
    kata_asing_id: int, limit: Optional[int] = None
) -> List[models.KataAsing]:
    return get_kata_asing_minimum_info(
        where=(models.KataAsing.id == kata_asing_id), limit=limit
    )


def delete_lemma(lemma: models.KataAsing) -> int:
    return lemma.delete_instance(recursive=False)
