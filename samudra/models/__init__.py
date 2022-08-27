"""
MODEL RELATIONSHIP REPRESENTATION
Lemma  <== Konsep <==> Cakupan
                  <==> KataAsing

--- Legend ---
One  <==   Many
Many <==>  Many
"""
# Ordered by table hierarchy
from .core.lemma import Lemma
from .core.konsep import Konsep, GolonganKata
from .core.cakupan import Cakupan, CakupanXKonsep
from .core.kata_asing import KataAsing, KataAsingXKonsep
from .auth.pengguna import Pengguna, Keizinan

# Imported for type hints
from .base import BaseDataTable

TABLES = [Lemma, Konsep, Cakupan, KataAsing, Pengguna, Keizinan, GolonganKata]

JOIN_TABLES = [CakupanXKonsep, KataAsingXKonsep]
