from samudra.database import Lemma
from samudra.database.models.cakupan import Cakupan, CakupanLemma
from samudra.database.models.lemma import LemmaAsing
from .mocks import mock_db

mock_lemma = {
    "nama": "mock",
    "golongan": "kata nama",
    "konsep": None,
}


class TestModels:
    def test_lemma(self):
        with mock_db.bind_ctx([Lemma], bind_refs=False):
            mock_db.create_tables([Lemma])
            q = Lemma.create(**mock_lemma)

        assert q.nama == mock_lemma['nama']
        assert q.golongan == mock_lemma['golongan']
        assert q.konsep == mock_lemma['konsep']

    def test_lemma_asing(self):
        with mock_db.bind_ctx([Lemma, LemmaAsing], bind_refs=False):
            mock_db.create_tables([Lemma, LemmaAsing])
            q = Lemma.create(**mock_lemma)

            mock_lemma_asing = {
                "nama": "mock_in_english",
                "golongan": "kata nama",
                "padanan_konsep": q
            }
            r = LemmaAsing.create(**mock_lemma_asing)
        assert q.nama == mock_lemma['nama']
        assert q.golongan == mock_lemma['golongan']
        assert q.konsep == mock_lemma['konsep']

        assert r.nama == mock_lemma_asing['nama']
        assert r.golongan == mock_lemma_asing['golongan']
        assert r.padanan_konsep == mock_lemma_asing['padanan_konsep']

    def test_cakupan(self):
        with mock_db.bind_ctx([Lemma, Cakupan, CakupanLemma], bind_refs=False):
            mock_db.create_tables([Lemma, Cakupan, CakupanLemma])
            q = Lemma.create(**mock_lemma)

            mock_cakupan = {
                "nama": "cakupan_1",
                "keterangan": "ujian",
                'lemma': mock_lemma,
            }
            r = Cakupan.create(**mock_cakupan)
        assert q.nama == mock_lemma['nama']
        assert q.golongan == mock_lemma['golongan']
        assert q.konsep == mock_lemma['konsep']

        assert r.nama == mock_cakupan['nama']
        assert r.keterangan == mock_cakupan['keterangan']
        assert r.lemma == mock_cakupan['lemma']
