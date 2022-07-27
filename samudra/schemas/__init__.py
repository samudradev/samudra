"""
MODEL RELATIONSHIP REPRESENTATION
Lemma  <== Konsep <== Cakupan
                  <== KataAsing
"""
# Ordered by table hierarchy
from samudra.schemas.tables.lemma import LemmaResponse
from samudra.schemas.tables.konsep import KonsepResponse

from samudra.schemas.input.annotated_text import AnnotatedText
