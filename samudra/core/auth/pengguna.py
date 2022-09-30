"""Functions relating to the management of [`Pengguna`][samudra.models.auth.Pengguna]
"""

from peewee import prefetch

from samudra import models

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Gets the hash of a given password

    Args:
        password (str): Raw password given by the user.

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that the password is correct

    Args:
        plain_password (str): Raw password given by the user.
        hashed_password (str): Hashed password given by [`get_password_hash`][samudra.core.auth.pengguna.get_password_hash]

    Returns:
        bool: Verification status
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_pengguna_by_nama(nama: str) -> models.Pengguna:
    """Gets a single row of [`Pengguna`][samudra.models.auth.Pengguna] by its username.

    Args:
        nama (str): username

    Returns:
        models.Pengguna: [`Pengguna`][samudra.models.auth.Pengguna]
    """
    return prefetch(models.Pengguna.get(models.Pengguna.nama == nama))


def create_pengguna(nama: str, katalaluan: str, safe: bool = True) -> models.Pengguna:
    """Creates a single row of [`Pengguna`][samudra.models.auth.Pengguna]

    Args:
        nama (str): username
        katalaluan (str): password
        safe (bool, optional): Try to get the existing row before creating. Defaults to True.

    Returns:
        models.Pengguna: [`Pengguna`][samudra.models.auth.Pengguna]
    """
    if safe:
        return models.Pengguna.get_or_create(
            nama=nama, kunci=get_password_hash(katalaluan)
        )[0]
    return models.Pengguna.create(nama=nama, kunci=get_password_hash(katalaluan))


def authenticate_pengguna(nama: str, katalaluan: str) -> models.Pengguna:
    """Authenticates a user

    Args:
        nama (str): username
        katalaluan (str): password

    Returns:
        models.Pengguna: [`Pengguna`][samudra.models.auth.Pengguna]
    """
    pengguna: models.Pengguna = get_pengguna_by_nama(nama)
    if not pengguna:
        return False
    if not verify_password(katalaluan, pengguna.kunci):
        return False
    return pengguna
