"""
MODEL RELATIONSHIP REPRESENTATION
Lemma  <== Konsep <== Cakupan
                  <== KataAsing
"""
# Ordered by table hierarchy
from samudra.schemas.tables.lemma import LemmaResponse
from samudra.schemas.tables.konsep import (
    KonsepResponseFromTables,
    KonsepResponseFromAnnotatedBody,
)

from samudra.schemas.input.annotated_text import AnnotatedText

from samudra.schemas.tables.user import LogMasukResponse, DaftarResponse

from samudra.schemas.tables.golongan_kata import CreateGolonganKata
