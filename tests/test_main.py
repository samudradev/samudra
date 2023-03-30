import peewee as pw
from samudra.interfaces import KonsepBuilder

from samudra.models.base import database_proxy as proxy
from samudra.models import Lemma, Konsep, Cakupan, KataAsing, GolonganKata

proxy.initialize(pw.SqliteDatabase(":memory:"))


def connect_test_database(function: callable, *args, **kwargs) -> callable:
    """Decorator to open and close a test database connection"""

    def wrapper():
        try:
            proxy.create_tables([Lemma, Konsep, Cakupan, KataAsing, GolonganKata])
            function(*args, **kwargs)
        finally:
            proxy.close()  # All data in `:memory:` database are deleted automatically once closed

    return wrapper


@connect_test_database
def test_konsep_builder():
    """Testing query for konsep"""
    Lemma.create(nama="nama")
    lem = Lemma.get(nama="nama")
    GolonganKata.create(id="NAMA", nama="nama", keterangan="...")
    gol = GolonganKata.get(id="NAMA")
    Konsep.create(lemma=lem, golongan=gol, keterangan="keterangan")
    query = KonsepBuilder(konsep="keterangan").get_lemma().query()
    assert query.keterangan == "keterangan"
    assert query.lemma.nama == "nama"
    assert query.golongan.nama == "nama"
