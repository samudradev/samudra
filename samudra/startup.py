from typing import List

import peewee

from samudra.models.base import database_proxy
from samudra.models import Lemma, Konsep, Cakupan, KataAsing
from samudra.conf.database.core import get_active_database


def bind_proxy_with_active_database(proxy: peewee.Database) -> peewee.Database:
    proxy.initialize(get_active_database())
    return proxy


def on_start() -> None:
    database = bind_proxy_with_active_database(proxy=database_proxy)
    database.create_tables([Lemma, Konsep, Cakupan, KataAsing], bind_refs=True)
