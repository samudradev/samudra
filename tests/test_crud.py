import tests.mocks as mocks
from samudra import models
from samudra.tools import crud


@mocks.bind_test_database
def test_create_lemma():
    new_lemma = mocks.TestLemma().to_schema
    # test non-existence before creating
    assert models.Lemma.get_or_none(models.Lemma.nama == new_lemma.nama) is None
    crud.create_lemma(new_lemma)
    # test existence after creating
    assert models.Lemma.get_or_none(models.Lemma.nama == new_lemma.nama)


@mocks.bind_test_database
def test_get_lemma():
    new_lemma = mocks.TestLemma().to_schema
    # test non-existence before creating
    assert models.Lemma.get_or_none(models.Lemma.nama == new_lemma.nama) is None
    crud.create_lemma(new_lemma)
    # test existence after creating
    assert crud.get_lemma_by_name(nama=new_lemma.nama)


@mocks.bind_test_database
def test_get_all_lemma():
    new_lemma = mocks.TestLemma().to_schema
    # test non-existence before creating
    assert models.Lemma.get_or_none(models.Lemma.nama == new_lemma.nama) is None
    crud.create_lemma(new_lemma)
    assert crud.get_all_lemma()[0].nama == new_lemma.nama
