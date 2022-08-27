from peewee import prefetch

from samudra import models

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_pengguna_by_nama(nama: str):
    return prefetch(models.Pengguna.get(models.Pengguna.nama == nama))


def create_pengguna(nama: str, katalaluan: str, safe: bool = True) -> models.Pengguna:
    if safe:
        return models.Pengguna.get_or_create(
            nama=nama, kunci=get_password_hash(katalaluan)
        )[0]
    return models.Pengguna.create(nama=nama, kunci=get_password_hash(katalaluan))


def authenticate_pengguna(nama: str, katalaluan: str):
    pengguna = get_pengguna_by_nama(nama)
    if not pengguna:
        return False
    if not verify_password(katalaluan, pengguna.kunci):
        return False
    return pengguna
