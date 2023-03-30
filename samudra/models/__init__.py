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

from samudra.models.core.lemma import Lemma
from samudra.models.core.konsep import Konsep, GolonganKata
from samudra.models.core.cakupan import Cakupan
from samudra.models.core.kata_asing import KataAsing
