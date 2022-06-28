from samudra.database import Lemma
from samudra.database.transactions.search import search_lemma
from tests.mocks import mock_db


def test_search_lemma():
    mock_lemma_1 = {
        "nama": "lemma_1",
        "golongan": "kata sifat",
        "keterangan": "Ini lemma 1"
    }
    mock_lemma_2 = {
        "nama": "lemma_2",
        "golongan": "kata nama",
        "keterangan": "Ini lemma 2"
    }
    mock_lemma_3 = {
        "nama": "entah",
        "golongan": "kata nama",
        "keterangan": "Ini tak nak"
    }
    with mock_db.bind_ctx([Lemma], bind_refs=False):
        mock_db.create_tables([Lemma])
        Lemma.create(**mock_lemma_1)
        Lemma.create(**mock_lemma_2)
        Lemma.create(**mock_lemma_3)
        q = search_lemma("lemma")
    assert "entah" not in [lemma.nama for lemma in q]

