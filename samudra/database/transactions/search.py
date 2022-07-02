from typing import List

from samudra.database import Konsep


def search_lemma(lemma: str, limit: int = None) -> List[Konsep]:
    # TODO: test_search_lemma
    return [item for item in Konsep.select().where(Konsep.lemma.contains(lemma)).limit(limit)]
