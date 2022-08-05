"""
MODEL RELATIONSHIP REPRESENTATION
Lemma  <== Konsep <==> Cakupan
                  <==> KataAsing

--- Legend ---
One  <==   Many
Many <==>  Many
"""
# Ordered by table hierarchy
from .lemma import Lemma
from .konsep import Konsep
from .cakupan import Cakupan, CakupanXKonsep
from .kata_asing import KataAsing, KataAsingXKonsep
from .user import User

# Imported for type hints
from .base import BaseTable

TABLES = [
    Lemma,
    Konsep,
    Cakupan,
    KataAsing,
    User
]

JOIN_TABLES = [
    CakupanXKonsep,
    KataAsingXKonsep
]
