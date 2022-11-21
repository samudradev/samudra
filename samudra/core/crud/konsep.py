from typing import Any, List, Dict

from peewee import prefetch

from samudra import models, schemas
from samudra.core.crud.lemma import create_lemma


def create_konsep(
    lemma: str,
    concept: str,
    golongan: str,
    tags: List[str],
    foreign: Dict[str, List[str]],
    force_lemma: bool = False,
) -> models.Konsep:
    golongan_ = models.GolonganKata.get_or_none(id=golongan.upper())
    if golongan_ is None:
        raise ValueError(
            f"The value '{golongan}' is not in models.{models.GolonganKata.__name__}. Consider adding one manually."
        )
    konsep = models.Konsep.create(
        keterangan=concept,
        lemma=create_lemma(lemma=lemma, force=force_lemma),
        golongan=golongan_,
    )
    if tags:
        konsep.attach(
            to_model=models.Cakupan,
            values=[{"nama": tag} for tag in tags],
        )
    if foreign:
        for lang in foreign.keys():
            konsep.attach(
                to_model=models.KataAsing,
                values=[{"nama": kata, "bahasa": lang} for kata in foreign[lang]],
            )
    return konsep


def create_konsep_by_annotated_text(
    annotated_text: schemas.AnnotatedText, lemma_name: str, force_lemma: bool = False
) -> models.Konsep:
    fields = annotated_text.fields
    return create_konsep(
        lemma=lemma_name,
        concept=annotated_text.content,
        golongan=fields.get("meta").get("gol"),
        tags=annotated_text.tags,
        foreign=fields.get("lang"),
    )


def get_konsep_minimum_info(where: Any, limit: int = None) -> List[models.Konsep]:
    stmt = models.Konsep.select(models.Konsep).where(where).limit(limit)
    to_return = prefetch(
        stmt,
        models.CakupanXKonsep,
        models.Cakupan,
        models.KataAsingXKonsep,
        models.KataAsing,
    )
    return to_return
