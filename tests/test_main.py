import functools
import peewee as pw
import pytest
from samudra.interfaces import (
    LemmaEditor,
    LemmaQueryBuilder,
    NewLemmaBuilder,
    new_golongan_kata,
)

from samudra.models.base import database_proxy as proxy
from samudra.models import (
    Lemma,
    Konsep,
    Cakupan,
    KataAsing,
    GolonganKata,
    CakupanXKonsep,
    KataAsingXKonsep,
)


@pytest.fixture
def create_data():
    proxy.create_tables(
        [
            Lemma,
            Konsep,
            Cakupan,
            KataAsing,
            GolonganKata,
            CakupanXKonsep,
            KataAsingXKonsep,
        ]
    )
    gol = new_golongan_kata(id="NAMA", nama="nama", keterangan="...")
    NewLemmaBuilder(konsep="keterangan", lemma="nama", golongan=gol.id).set_cakupan(
        nama="cakupan"
    ).save()


proxy.initialize(pw.SqliteDatabase(":memory:"))


def connect_test_database(function: callable, *args, **kwargs) -> callable:
    """Decorator to open and close a test database connection"""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        finally:
            proxy.close()  # All data in `:memory:` database are deleted automatically once closed

    return wrapper


@connect_test_database
def test_lemma_query(create_data):
    """Testing query for konsep"""
    # Test query of both konsep and lemma
    query = LemmaQueryBuilder(konsep="keterangan", lemma="nama").get_cakupan().collect()
    assert query.nama == "nama"
    assert query.konsep[0].keterangan == "keterangan"
    assert query.konsep[0].golongan.nama == "nama"
    assert query.konsep[0].cakupan[0].cakupan.nama == "cakupan"

    # Test query of konsep
    query = LemmaQueryBuilder(konsep="keterangan").get_cakupan().collect()
    assert query.nama == "nama"
    assert query.konsep[0].keterangan == "keterangan"
    assert query.konsep[0].golongan.nama == "nama"

    # Test query of lemma
    query = LemmaQueryBuilder(lemma="nama").get_cakupan().collect()
    assert query.nama == "nama"
    assert query.konsep[0].keterangan == "keterangan"
    assert query.konsep[0].golongan.nama == "nama"

    # Test query with no matching instance
    query = LemmaQueryBuilder(lemma="nm").get_cakupan().collect()
    assert query == None

    # Test assert kwargs only
    with pytest.raises(TypeError):
        # Ambiguity: Are you querying for lemma or konsep?
        LemmaQueryBuilder("nm")

    # Test None query raise ValueError
    with pytest.raises(ValueError):
        LemmaQueryBuilder(konsep=None, lemma=None)


@connect_test_database
def test_lemma_editor(create_data):
    query = LemmaQueryBuilder(konsep="keterangan", lemma="nama").collect()
    assert query.nama == "nama"

    # Test edit lemma
    newlemma = LemmaEditor(query)
    newlemma.rename("baharu").save()
    assert LemmaQueryBuilder(lemma="nama").collect() is None

    # Test edit konsep
    query = LemmaQueryBuilder(konsep="keterangan", lemma="baharu").collect()
    assert query.nama == "baharu"
    edit = LemmaEditor(query)
    edit.rewrite_konsep(0, "ujian suntingan").save()
    assert LemmaQueryBuilder(konsep="keterangan").collect() is None
