from typing import List

from samudra.database import Lemma


def search_lemma(lemma: str, limit: int = None) -> List[Lemma]:
    # TODO: test_search_lemma
    return [item for item in Lemma.select().where(Lemma.nama.contains(lemma)).limit(limit)]
