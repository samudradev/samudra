from peewee import prefetch

from samudra import models

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(username: str):
    return prefetch(models.User.get(models.User.username == username))

def create_user(username: str, password: str, safe: bool = True) -> models.User:
    if safe:
        return models.User.get_or_create(username=username, password_hash=get_password_hash(password))[0]
    return models.User.create(username=username, password_hash=get_password_hash(password))

def authenticate_user(username: str, password: str):
    user = get_user_by_username(username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user