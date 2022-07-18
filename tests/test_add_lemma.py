from .mocks import mock_db


class TestTransactions:
    def test_add_lemma(self):
        from samudra.database import Konsep
        from samudra.database.transactions.add import add_lemma
        mock_concept = dict(lemma='lemma', golongan='nama', konsep=None)
        mock_db.bind([Konsep], bind_refs=False, bind_backrefs=False)
        mock_db.create_tables([Konsep])
        add_lemma(**mock_concept)
        q = Konsep.get_or_none(Konsep.lemma == mock_concept['lemma'])

        mock_db.close()
        assert q.lemma == mock_concept['lemma']
        assert q.golongan == mock_concept['golongan']
        assert q.keterangan == mock_concept['konsep']
