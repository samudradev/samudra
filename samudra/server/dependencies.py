from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from samudra.server.setup import SERVER_DATABASE
from samudra.conf.database.core import db_state_default


async def reset_db_state() -> None:
    """Resetting Database state for a fresh query"""
    try:
        SERVER_DATABASE._state._state.set(db_state_default.copy())
        SERVER_DATABASE._state.reset()
    except AttributeError:
        pass


def get_db(db_state=Depends(reset_db_state)):
    """Gets the database for a server route.

    !!! important "TODO"
        As of now, I do not know how to override this for testing.
    """
    try:
        SERVER_DATABASE.connect()
        yield
    finally:
        if not SERVER_DATABASE.is_closed():
            SERVER_DATABASE.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
