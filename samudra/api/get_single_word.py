from dataclasses import dataclass, asdict
from typing import Optional, List

from samudra.database.models import Konsep


@dataclass
class SingleConcept:
    golongan: str
    keterangan: str = None
    nombor_semantik: Optional[str] = None
    tertib: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class SingleWord:
    lemma: str

    def to_dict(self) -> dict:
        return {
            "lemma": self.lemma,
            "konsep": [konsep.to_dict() for konsep in self.concepts]
        }

    @property
    def concepts(self) -> List[SingleConcept]:
        concepts = [*Konsep().select(Konsep.golongan, Konsep.keterangan, Konsep.nombor_semantik, Konsep.tertib).where(
            Konsep.lemma == self.lemma)]
        return [*self.yield_concepts(concepts)]

    @staticmethod
    def yield_concepts(concepts) -> [SingleConcept]:
        for concept in concepts:
            yield SingleConcept(golongan=concept.golongan, keterangan=concept.keterangan.decode('UTF-8'),
                                nombor_semantik=concept.nombor_semantik, tertib=concept.tertib)
