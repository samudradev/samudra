from samudra.api.get_single_word import SingleWord
from samudra.database.models import Konsep
from tests.mocks import mock_db


class TestSingleWord:
    def test_single_word(self):
        mock_concept_1 = {
            "lemma": "lemma_1",
            "golongan": "kata nama",
            "keterangan": "Ini lemma 1"
        }
        mock_concept_2 = {
            "lemma": "lemma_1",
            "golongan": "kata sifat",
            "keterangan": "Ini sifat lemma 1"
        }
        with mock_db.bind_ctx([Konsep], bind_refs=False):
            mock_db.create_tables([Konsep], safe=False)
            Konsep.create(**mock_concept_1)
            Konsep.create(**mock_concept_2)

            single_word = SingleWord(lemma="lemma_1")

        assert single_word.concepts[0].golongan == 'kata nama'
        assert single_word.concepts[1].golongan == 'kata sifat'
        assert single_word.concepts[0].keterangan == 'Ini lemma 1'
        assert single_word.concepts[1].keterangan == 'Ini sifat lemma 1'

    def test_dictionary_representation(self):
        mock_concept_1 = {
            "lemma": "lemma_1",
            "golongan": "kata sifat",
            "keterangan": "Ini lemma 1"
        }
        mock_concept_2 = {
            "lemma": "lemma_1",
            "golongan": "kata nama",
            "keterangan": "Ini sifat lemma 1"
        }
        with mock_db.bind_ctx([Konsep], bind_refs=False):
            # TODO: Make sure that db connection is properly isolated per methods
            # mock_db.create_tables([Konsep], safe=False)
            # Konsep.create(**mock_lemma_1)
            # Konsep.create(**mock_lemma_2)

            single_word = SingleWord(lemma="lemma_1")

        assert single_word.to_dict() == {
            "lemma": "lemma_1",
            "konsep": [
                {"golongan": "kata nama", "keterangan": "Ini lemma 1", "nombor_semantik": None, "tertib": None},
                {"golongan": "kata sifat", "keterangan": "Ini sifat lemma 1", "nombor_semantik": None, "tertib": None}
            ]
        }
