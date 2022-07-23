"""
MODEL RELATIONSHIP REPRESENTATION
Lemma  <== Konsep <== Cakupan
                  <== KataAsing
"""
# Ordered by table hierarchy
from .lemma import LemmaResponse
from .konsep import KonsepResponse
from .cakupan import CakupanResponse
from .kata_asing import KataAsingResponse

from .annotated_text import AnnotatedText
