from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware

from samudra.main import app
from samudra.conf import Database
from samudra.conf.database import db_state_default

SLEEP_TIME: int = 10

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


async def reset_db_state() -> None:
    Database.connection._state._state.set(db_state_default.copy())
    Database.connection._state.reset()


def get_db(db_state=Depends(reset_db_state)):
    try:
        Database.connection.connect()
        yield
    finally:
        if not Database.connection.is_closed():
            Database.connection.close()
