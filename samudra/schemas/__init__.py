"""Schema to structure data within application.

!!! warning
    This schema is still a mess. 
    I hope to reorganize it one day. 
    As such, I put off documenting it now as I prioritize other docs.
"""

from samudra.schemas.input.annotated_text import AnnotatedText
from samudra.schemas.tables.golongan_kata import CreateGolonganKata
from samudra.schemas.tables.konsep import (
    KonsepResponseFromTables,
    KonsepResponseFromAnnotatedBody,
)

# Ordered by table hierarchy
from samudra.schemas.tables.lemma import LemmaResponse
from samudra.schemas.tables.user import LogMasukResponse, DaftarResponse
