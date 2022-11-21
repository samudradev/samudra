from typing import List, Optional, Any

from peewee import prefetch

from samudra import models
from samudra.schemas.input.query_filter import QueryFilter


def create_lemma(lemma: str, force: bool = False) -> models.Lemma:
    if force:
        return models.Lemma.create(nama=lemma)
    value, exists = models.Lemma.get_or_create(nama=lemma)
    return value


def get_lemma_minimum_info(
    query: Optional[QueryFilter] = None, where: Any = None
) -> List[models.Lemma]:
    query: QueryFilter = QueryFilter(**query.dict())
    stmt = models.Lemma.select().where(where)

    to_return = prefetch(
        stmt,
        models.Konsep,
        models.CakupanXKonsep,
        models.Cakupan.select().where(
            (
                models.Cakupan.nama.in_(query.cakupan)
                if query.cakupan is not None
                else None
            )
        ),
        models.KataAsingXKonsep,
        models.KataAsing.select().where(
            (
                models.KataAsing.nama.in_(query.kata_asing)
                if query.kata_asing is not None
                else None
            )
        ),
    )
    return to_return


def get_lemma(query: QueryFilter) -> List[models.Lemma]:
    return get_lemma_minimum_info(query=query)


def get_lemma_by_name(nama: str, query: QueryFilter) -> List[models.Lemma]:
    return get_lemma_minimum_info(where=models.Lemma.nama == nama, query=query)


def get_lemma_by_id(lemma_id: int, query: QueryFilter) -> List[models.Lemma]:
    return get_lemma_minimum_info(where=(models.Lemma.id == lemma_id), query=query)


def delete_lemma(lemma: models.Lemma) -> int:
    return lemma.delete_instance(recursive=True)
