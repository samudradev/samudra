from samudra import models


def count_lemma() -> int:
    return len(models.Lemma.select(models.Lemma.id))
