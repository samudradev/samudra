"""
MODEL RELATIONSHIP REPRESENTATION
Lemma  <== Konsep <==> Cakupan
                  <==> KataAsing

--- Legend ---
One  <==   Many
Many <==>  Many
"""
# Ordered by table hierarchy
from models.core.lemma import Lemma
from models.core.konsep import Konsep
from models.core.cakupan import Cakupan, CakupanXKonsep
from models.core.kata_asing import KataAsing, KataAsingXKonsep
from models.auth.pengguna import Pengguna

# Imported for type hints
from .base import BaseTable

TABLES = [Lemma, Konsep, Cakupan, KataAsing, Pengguna]

JOIN_TABLES = [CakupanXKonsep, KataAsingXKonsep]
