from typing import Any, Optional, List

from peewee import prefetch

from samudra import models


def get_cakupan_minimum_info(
    where: Any, limit: Optional[int] = None
) -> List[models.Cakupan]:
    stmt = models.Cakupan.select(models.Cakupan).where(where).limit(limit)
    to_return = prefetch(stmt, models.CakupanXKonsep, models.Konsep, models.Lemma)
    return to_return


def get_cakupan(limit: int = 10) -> List[models.Cakupan]:
    return get_cakupan_minimum_info(where=None, limit=limit)


def get_cakupan_by_name(nama: str, limit: int = 1) -> List[models.Cakupan]:
    return get_cakupan_minimum_info(where=models.Cakupan.nama == nama, limit=limit)


def get_cakupan_by_id(
    cakupan_id: int, limit: Optional[int] = None
) -> List[models.Cakupan]:
    return get_cakupan_minimum_info(
        where=(models.Cakupan.id == cakupan_id), limit=limit
    )


def delete_lemma(lemma: models.Cakupan) -> int:
    return lemma.delete_instance(recursive=False)
