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
from typing import List

import peewee

from .base import BaseDataTable

# Ordered by table hierarchy
from .core.lemma import Lemma
from .core.konsep import Konsep, GolonganKata
from .core.cakupan import Cakupan, CakupanXKonsep
from .core.kata_asing import KataAsing, KataAsingXKonsep
from .auth.pengguna import Pengguna, Keizinan
from .experimental.petikan import Petikan, PetikanXKonsep, SumberPetikan

TABLES = [Lemma, Konsep, Cakupan, KataAsing, Pengguna, Keizinan, GolonganKata]

JOIN_TABLES = [CakupanXKonsep, KataAsingXKonsep]


def create_tables(
    database: peewee.Database,
    auth: bool = True,
    foreign_lang: bool = True,
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
    tables: List[peewee.Model] = []
    tables.extend([Lemma, Konsep, GolonganKata, Cakupan, CakupanXKonsep])
    if foreign_lang:
        tables.extend([KataAsing, KataAsingXKonsep])
    if auth:
        tables.extend([Pengguna, Keizinan])
    if experimental:
        tables.extend([Petikan, PetikanXKonsep, SumberPetikan])
    database.bind(tables)
    database.create_tables(tables)
    # TODO logging
    return database.get_tables()
