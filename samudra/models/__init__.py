"""Module that contains SQL Tables known as models.

- [🏠 Base][samudra.models.base]
- [💡 Core][samudra.models.core]
- [🔐 Auth][samudra.models.auth]
- [🧪 Experimental][samudra.models.experimental]
"""

# MODEL RELATIONSHIP REPRESENTATION
# ```
# Lemma  <== Konsep <==> Cakupan
#                   <==> KataAsing

# --- Legend ---
# One  <==   Many
# Many <==>  Many
# ```
from typing import List, Type

import peewee

from .base import BaseDataTable

# Ordered by table hierarchy
from .core.lemma import Lemma
from .core.konsep import Konsep, GolonganKata
from .core.cakupan import Cakupan, CakupanXKonsep
from .core.kata_asing import KataAsing, KataAsingXKonsep
from .auth.pengguna import Pengguna, Keizinan
from .experimental.petikan import Petikan, PetikanXKonsep, SumberPetikan


def create_tables(
    database: peewee.Database,
    auth: bool = True,
    experimental: bool = False,
) -> List[str]:
    """Create tables based on selected criteria

    Args:
        database (peewee.Database): The database engine to bind the models
        auth (bool, optional): Whether to include auth tables or not. Defaults to True
        foreign_lang (bool, optional): Whether to include foreign lang tables or not. Defaults to True
        experimental (bool, optional): Whether to include experimental tables or not. Defaults to False

    Returns:
        List of tables created
    """
    tables = bind_to_database(database, auth, experimental)
    database.create_tables(tables)
    # TODO logging
    return database.get_tables()


def bind_to_database(
    database: peewee.Database, auth: bool = True, experimental: bool = False
):
    tables: List[Type[peewee.Model]] = []
    tables.extend([Lemma, Konsep, GolonganKata, *Cakupan.with_dependencies()])
    tables.extend([*KataAsing.with_dependencies()])
    if auth:
        tables.extend([Pengguna, Keizinan])
    if experimental:
        tables.extend([Petikan, PetikanXKonsep, SumberPetikan])
    database.bind(tables)
    return tables
