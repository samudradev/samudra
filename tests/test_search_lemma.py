from samudra.database import Konsep
from samudra.database.transactions.search import search_lemma
from tests.mocks import mock_db


def test_search_lemma():
    mock_concept_1 = {
        "lemma": "lemma_1",
        "golongan": "kata sifat",
        "keterangan": "Ini lemma 1"
    }
    mock_concept_2 = {
        "lemma": "lemma_2",
        "golongan": "kata nama",
        "keterangan": "Ini lemma 2"
    }
    mock_concept_3 = {
        "lemma": "entah",
        "golongan": "kata nama",
        "keterangan": "Ini tak nak"
    }
    with mock_db.bind_ctx([Konsep], bind_refs=False):
        mock_db.create_tables([Konsep])
        Konsep.create(**mock_concept_1)
        Konsep.create(**mock_concept_2)
        Konsep.create(**mock_concept_3)
        q = search_lemma("lemma")
    assert "entah" not in [lemma.lemma for lemma in q]
