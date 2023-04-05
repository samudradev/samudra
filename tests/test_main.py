import functools
import peewee as pw
import pytest
from samudra.interfaces import LemmaQueryBuilder, NewLemmaBuilder, new_golongan_kata

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

proxy.initialize(pw.SqliteDatabase(":memory:"))


@pytest.fixture
def create_data():
    gol = new_golongan_kata(id="NAMA", nama="nama", keterangan="...")
    NewLemmaBuilder(konsep="keterangan", lemma="nama", golongan=gol.id).save()


def connect_test_database(function: callable, *args, **kwargs) -> callable:
    """Decorator to open and close a test database connection"""
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

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        finally:
            proxy.close()  # All data in `:memory:` database are deleted automatically once closed

    return wrapper


@connect_test_database
def test_konsep_builder(create_data):
    """Testing query for konsep"""
    # Test query of both konsep and lemma
    query = LemmaQueryBuilder(konsep="keterangan", lemma="nama").get_cakupan().collect()
    assert query.keterangan == "keterangan"
    assert query.lemma.nama == "nama"
    assert query.golongan.nama == "nama"

    # Test query of konsep
    query = LemmaQueryBuilder(konsep="keterangan").get_cakupan().collect()
    assert query.keterangan == "keterangan"
    assert query.lemma.nama == "nama"
    assert query.golongan.nama == "nama"

    # Test query of lemma
    query = LemmaQueryBuilder(lemma="nama").get_cakupan().collect()
    assert query.keterangan == "keterangan"
    assert query.lemma.nama == "nama"
    assert query.golongan.nama == "nama"

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
