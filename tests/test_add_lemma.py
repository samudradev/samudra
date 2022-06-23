from .mocks import mock_db


class TestTransactions:
    def test_add_lemma(self):
        from samudra.database import Lemma
        from samudra.database.transactions.add import add_lemma
        mock_lemma = dict(nama='lemma', golongan='nama', konsep=None)
        mock_db.bind([Lemma], bind_refs=False, bind_backrefs=False)
        mock_db.create_tables([Lemma])
        add_lemma(**mock_lemma)
        q = Lemma.get_or_none(Lemma.nama == mock_lemma['nama'])

        mock_db.close()
        assert q.nama == mock_lemma['nama']
        assert q.golongan == mock_lemma['golongan']
        assert q.konsep == mock_lemma['konsep']
