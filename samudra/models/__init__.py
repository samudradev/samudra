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

# Ordered by table hierarchy
from .core.lemma import Lemma
from .core.konsep import Konsep, GolonganKata
from .core.cakupan import Cakupan, CakupanXKonsep
from .core.kata_asing import KataAsing, KataAsingXKonsep
from .auth.pengguna import Pengguna, Keizinan

TABLES = [Lemma, Konsep, Cakupan, KataAsing, Pengguna, Keizinan, GolonganKata]

JOIN_TABLES = [CakupanXKonsep, KataAsingXKonsep]
