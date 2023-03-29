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


def create_tables(
    database: peewee.Database,
    auth: bool = True,
    experimental: bool = False,
) -> List[str]:
    """Create tables based on selected criteria

    Args:
        database (peewee.Database): The database engine to bind the models
        auth (bool, optional): Whether to include auth tables or not. Defaults to True
        experimental (bool, optional): Whether to include experimental tables or not. Defaults to False

    Returns:
        List of tables created
    """
    tables = database.get_tables()
    database.create_tables(tables)
    # TODO logging
    return database.get_tables()
