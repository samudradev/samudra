from samudra.conf.setup import bind_proxy_to_database

from samudra.models.base import database_proxy
from samudra.models import create_tables


def on_start() -> None:
    database = bind_proxy_to_database(proxy=database_proxy)
    create_tables(database=database)


def on_shutdown() -> None:
    ...


if __name__ == "__main__":
    print(
        "The current codebase is written as a library. Please do not run this as a script."
    )
