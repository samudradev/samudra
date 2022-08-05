from samudra import models
from samudra.core.crud.cakupan import get_cakupan_by_name
from samudra.core.crud.kata_asing import get_kata_asing_by_name
from samudra.core.crud.konsep import create_konsep, get_konsep_minimum_info
from samudra.core.crud.lemma import get_lemma_minimum_info
from samudra.core.crud.user import create_user, authenticate_user, get_user_by_username
from samudra.schemas import AnnotatedText
from tests import mocks
from passlib.context import CryptContext

DATA_1 = "Ini adalah konsep cubaan #tag_1 #tag-2 {lang.en:concept} {lang.en:test} {meta.gol:NAMA}"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@mocks.bind_test_database
def test_create_konsep():
    data = AnnotatedText(body=DATA_1)
    assert create_konsep(annotated_text=data, lemma_name='ujian').keterangan == "Ini adalah konsep cubaan"


@mocks.bind_test_database
def test_get_minimum_lemma_info():
    data = AnnotatedText(body=DATA_1)
    create_konsep(annotated_text=data, lemma_name='ujian')
    create_konsep(annotated_text=data, lemma_name='ujian')
    lemma = get_lemma_minimum_info(where=(mocks.Lemma.nama == 'ujian'), limit=1)[0]
    assert lemma.nama == 'ujian'
    assert lemma.id == 1
    assert len(lemma.konsep) == 2


@mocks.bind_test_database
def test_get_minimum_konsep_info():
    data = AnnotatedText(body=DATA_1)
    create_konsep(annotated_text=data, lemma_name='ujian')
    konsep = get_konsep_minimum_info(where=None, limit=None)
    assert konsep == list(models.Konsep)


@mocks.bind_test_database
def test_get_cakupan_by_name():
    data = AnnotatedText(body=DATA_1)
    create_konsep(annotated_text=data, lemma_name='ujian')
    cakupan = get_cakupan_by_name(nama='tag 1')
    assert cakupan[0].nama == 'tag 1'


@mocks.bind_test_database
def test_get_kata_asing_by_name():
    data = AnnotatedText(body=DATA_1)
    create_konsep(annotated_text=data, lemma_name='ujian')
    kata_asing = get_kata_asing_by_name(nama='concept')
    assert kata_asing[0].nama == 'concept'

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
