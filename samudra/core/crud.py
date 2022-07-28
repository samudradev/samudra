from typing import List, Optional, Any, Union

from peewee import prefetch

from samudra import models
from samudra import schemas


def get_minimum_lemma_info(where: Any, limit: Optional[int] = None) -> List[models.Lemma]:
    stmt = models.Lemma.select(models.Lemma).where(where).limit(limit)
    to_return = prefetch(stmt, models.Konsep)
    # TODO: Also return cakupan and kata asing
    return to_return


def get_lemma_by_name(nama: str, limit: int = 1) -> List[models.Lemma]:
    return get_minimum_lemma_info(where=models.Lemma.nama == nama, limit=limit)


def get_lemma_by_id(lemma_id: int, limit: Optional[int] = None) -> List[models.Lemma]:
    return get_minimum_lemma_info(where=(models.Lemma.id == lemma_id), limit=limit)


def get_all_lemma(limit: int = 10) -> List[models.Lemma]:
    return get_minimum_lemma_info(where=None, limit=limit)


def create_konsep(annotated_text: schemas.AnnotatedText, lemma_name: str) -> models.Konsep:
    konsep = models.Konsep.create(golongan=annotated_text.fields.get('meta').get('gol'),
                                  keterangan=annotated_text.content,
                                  lemma=models.Lemma.get_or_create(nama=lemma_name)[0])
    if annotated_text.tags:
        konsep.cakupan = [models.Cakupan.get_or_create(nama=tag)[0] for tag in annotated_text.tags]
    if annotated_text.fields.get('lang'):
        kata_asing_full = list()
        for lang in annotated_text.fields.get('lang'):
            kata_asing = [models.KataAsing.get_or_create(nama=nama, bahasa=lang)[0] for nama in
                          annotated_text.fields.get("lang")[lang]]
            kata_asing_full.extend(kata_asing)
        konsep.kata_asing = kata_asing_full
    return konsep


def delete_lemma(lemma: models.Lemma) -> int:
    return lemma.delete_instance(recursive=True)


def get_all_konsep(limit: int = None) -> List[models.Konsep]:
    return models.Konsep.select(models.Konsep).limit(limit)
