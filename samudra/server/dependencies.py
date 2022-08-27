from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from samudra.conf import Database
from samudra.conf.database.core import db_state_default


async def reset_db_state() -> None:
    try:
        Database.connection._state._state.set(db_state_default.copy())
        Database.connection._state.reset()
    except AttributeError:
        pass


def get_db(db_state=Depends(reset_db_state)):
    try:
        Database.connection.connect()
        yield
    finally:
        if not Database.connection.is_closed():
            Database.connection.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
