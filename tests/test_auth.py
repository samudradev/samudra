from samudra.core.auth.pengguna import create_pengguna, authenticate_pengguna, get_pengguna_by_nama
from tests import mocks
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@mocks.bind_test_database
def test_get_pengguna_by_nama():
    nama = 'pengguna'
    katalaluan = 'katalaluan123'
    pengguna = create_pengguna(nama=nama, katalaluan=katalaluan)

    assert get_pengguna_by_nama(nama).nama == pengguna.nama

@mocks.bind_test_database
def test_create_pengguna():
    nama = 'pengguna'
    katalaluan = 'katalaluan123'

    assert pwd_context.verify(katalaluan, create_pengguna(nama='pengguna', katalaluan='katalaluan123').kunci)

@mocks.bind_test_database
def test_authenticate_pengguna():
    create_pengguna(nama='pengguna', katalaluan='katalaluan123')

    assert authenticate_pengguna(nama='pengguna', katalaluan='katalaluan123')
