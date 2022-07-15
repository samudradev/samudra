"""
MODEL RELATIONSHIP REPRESENTATION
Lemma  <== Konsep <== Cakupan
                  <== KataAsing
"""
# Ordered by table hierarchy
from .lemma import LemmaCreation, LemmaRecord
from .konsep import KonsepCreation, KonsepRecord
from .cakupan import CakupanCreation, CakupanRecord
from .kata_asing import KataAsingCreation, KataAsingRecord
