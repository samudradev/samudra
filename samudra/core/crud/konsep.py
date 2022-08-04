from typing import Any, List

from peewee import prefetch

from samudra import models, schemas
from samudra.core.crud.lemma import create_lemma


def create_konsep(annotated_text: schemas.AnnotatedText, lemma_name: str) -> models.Konsep:
    konsep = models.Konsep.create(golongan=annotated_text.fields.get('meta').get('gol'),
                                  keterangan=annotated_text.content,
                                  lemma=create_lemma(lemma=lemma_name, safe=True))
    if annotated_text.tags:
        konsep.attach_cakupan(*annotated_text.tags)
    if annotated_text.fields.get('lang'):
        for lang in annotated_text.fields.get('lang'):
            [konsep.attach_kata_asing(kata_asing=nama, bahasa=lang) for nama in annotated_text.fields.get("lang")[lang]]
    return konsep


def get_konsep_minimum_info(where: Any, limit: int = None) -> List[models.Konsep]:
    stmt = models.Konsep.select(models.Konsep).where(where).limit(limit)
    to_return = prefetch(stmt, models.CakupanXKonsep, models.Cakupan, models.KataAsingXKonsep, models.KataAsing)
    return to_return
