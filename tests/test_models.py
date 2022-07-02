from samudra.database import Konsep
from samudra.database.models.cakupan import Cakupan, CakupanLemma
from samudra.database.models.kata_asing import KataAsing
from samudra.database.models.perwakilan_moden import JenisPerwakilanModen, PerwakilanModen
from .mocks import mock_db

mock_concept = {
    "lemma": "mock",
    "golongan": "kata nama",
    "konsep": None,
}


class TestModels:
    def test_lemma(self):
        with mock_db.bind_ctx([Konsep], bind_refs=False):
            mock_db.create_tables([Konsep])
            q = Konsep.create(**mock_concept)

        assert q.lemma == mock_concept['lemma']
        assert q.golongan == mock_concept['golongan']
        assert q.keterangan == mock_concept['konsep']

    def test_lemma_asing(self):
        with mock_db.bind_ctx([Konsep, KataAsing], bind_refs=False):
            mock_db.create_tables([Konsep, KataAsing])
            q = Konsep.create(**mock_concept)

            mock_lemma_asing = {
                "lemma": "mock_in_english",
                "golongan": "kata nama",
                "konsep": q
            }
            r = KataAsing.create(**mock_lemma_asing)
        assert q.lemma == mock_concept['lemma']
        assert q.golongan == mock_concept['golongan']
        assert q.keterangan == mock_concept['konsep']

        assert r.lemma == mock_lemma_asing['lemma']
        assert r.golongan == mock_lemma_asing['golongan']
        assert r.konsep == mock_lemma_asing['konsep']

    def test_cakupan(self):
        with mock_db.bind_ctx([Konsep, Cakupan, CakupanLemma], bind_refs=False):
            mock_db.create_tables([Konsep, Cakupan, CakupanLemma])
            q = Konsep.create(**mock_concept)

            mock_cakupan = {
                "nama": "cakupan_1",
                "keterangan": "ujian",
                'lemma': mock_concept,
            }
            r = Cakupan.create(**mock_cakupan)
        assert q.lemma == mock_concept['lemma']
        assert q.golongan == mock_concept['golongan']
        assert q.keterangan == mock_concept['konsep']

        assert r.nama == mock_cakupan['nama']
        assert r.keterangan == mock_cakupan['keterangan']
        assert r.lemma == mock_cakupan['lemma']

    def test_perwakilan_moden(self):
        with mock_db.bind_ctx([Konsep, PerwakilanModen, JenisPerwakilanModen], bind_refs=False):
            mock_db.create_tables([Konsep, PerwakilanModen, JenisPerwakilanModen])
            q = Konsep.create(**mock_concept)
            s = JenisPerwakilanModen.create(**{"nama": "rumus matematik"})
            mock_perwakilan = {
                "konsep": q,
                "jenis": s,
                "keterangan": "$F=ma$",
            }
            r = PerwakilanModen.create(**mock_perwakilan)
        assert q.lemma == mock_concept['lemma']
        assert q.golongan == mock_concept['golongan']
        assert q.keterangan == mock_concept['konsep']

        assert r.konsep == mock_perwakilan['konsep']
        assert r.jenis == mock_perwakilan['jenis']
        assert r.keterangan == mock_perwakilan['keterangan']
