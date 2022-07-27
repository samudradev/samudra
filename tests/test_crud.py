from samudra.schemas import AnnotatedText
from samudra.core import crud
from tests import mocks

DATA_1 = "Ini adalah konsep cubaan #tag_1 #tag-2 {lang.en:concept} {lang.en:test} {meta.gol:NAMA}"


@mocks.bind_test_database
def test_create_konsep():
    data = AnnotatedText(body=DATA_1)
    assert crud.create_konsep(annotated_text=data, lemma_name='ujian').keterangan == "Ini adalah konsep cubaan"


@mocks.bind_test_database
def test_get_minimum_lemma_info():
    data = AnnotatedText(body=DATA_1)
    crud.create_konsep(annotated_text=data, lemma_name='ujian')
    crud.create_konsep(annotated_text=data, lemma_name='ujian')
    lemma = crud.get_minimum_lemma_info(where=(mocks.Lemma.nama == 'ujian'), limit=1)[0]
    assert lemma.nama == 'ujian'
    assert lemma.id == 1
    assert len(lemma.konsep) == 2
