from samudra.database import Lemma
from samudra.database.models.lemma import LemmaAsing
from .mocks import mock_db


class TestModels:
    def test_lemma(self):
        mock_lemma = {
            "nama": "mock",
            "golongan": "kata nama",
            "konsep": None,
        }
        mock_db.bind([Lemma], bind_refs=False)
        mock_db.create_tables([Lemma])
        q = Lemma.create(**mock_lemma)

        mock_db.close()
        assert q.nama == mock_lemma['nama']
        assert q.golongan == mock_lemma['golongan']
        assert q.konsep == mock_lemma['konsep']

    def test_lemma_asing(self):
        mock_lemma = {
            "nama": "mock",
            "golongan": "kata nama",
            "konsep": None,

        }
        mock_db.bind([Lemma, LemmaAsing])
        mock_db.create_tables([Lemma, LemmaAsing])
        q = Lemma.create(**mock_lemma)

        mock_lemma_asing = {
            "nama": "mock_in_english",
            "golongan": "kata nama",
            "padanan_konsep": q
        }
        r = LemmaAsing.create(**mock_lemma_asing)

        mock_db.close()

        assert q.nama == mock_lemma['nama']
        assert q.golongan == mock_lemma['golongan']
        assert q.konsep == mock_lemma['konsep']

        assert r.nama == mock_lemma_asing['nama']
        assert r.golongan == mock_lemma_asing['golongan']
        assert r.padanan_konsep == mock_lemma_asing['padanan_konsep']

