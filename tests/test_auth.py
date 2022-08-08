from samudra.core.auth.user import create_user, authenticate_user, get_user_by_username
from tests import mocks
from passlib.context import CryptContext

DATA_1 = "Ini adalah konsep cubaan #tag_1 #tag-2 {lang.en:concept} {lang.en:test} {meta.gol:NAMA}"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@mocks.bind_test_database
def test_get_user_by_name():
    username = 'pengguna'
    password = 'katalaluan123'
    user = create_user(username=username, password=password)

    assert get_user_by_username(username).username == username

@mocks.bind_test_database
def test_create_user():
    username = 'pengguna'
    password = 'katalaluan123'

    assert pwd_context.verify(password, create_user(username=username, password=password).password_hash)

@mocks.bind_test_database
def test_authenticate_user():
    user = create_user(username='pengguna', password='katalaluan123')

    assert authenticate_user(username='pengguna', password='katalaluan123')
