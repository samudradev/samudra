import pytest

from samudra.core.crud.golongan_kata import create_golongan_kata
from samudra import models
from samudra.core.crud.cakupan import get_cakupan_by_name
from samudra.core.crud.kata_asing import get_kata_asing_by_name
from samudra.core.crud.konsep import (
    create_konsep_by_annotated_text,
    get_konsep_minimum_info,
)
from samudra.core.crud.lemma import get_lemma_minimum_info
from samudra.schemas import AnnotatedText, CreateGolonganKata
from samudra.schemas.input.query_filter import QueryFilter
from tests import mocks
from passlib.context import CryptContext

DATA_1 = "Ini adalah konsep cubaan #tag_1 #tag-2 {lang.en:concept} {lang.en:test} {meta.gol:NAMA}"


# TODO create wrappers for setup of each crud test


@mocks.bind_test_database
def test_create_golongan_kata():
    data = CreateGolonganKata(
        id="nama",
        nama="kata nama",
        keterangan="kata yang digunakan untuk merujuk kepada benda.",
    )
    create_golongan_kata(data=data)
    gol = models.GolonganKata.get_or_none(id="NAMA")
    assert gol.id == "NAMA"
    assert gol.nama == "Kata Nama"


@mocks.bind_test_database
def test_create_golongan_kata_w_value_error():
    with pytest.raises(ValueError):
        CreateGolonganKata(
            id="namayasa",
            nama="kata nama",
            keterangan="kata yang digunakan untuk merujuk kepada benda.",
        )


@mocks.bind_test_database
def test_create_konsep():
    data = AnnotatedText(body=DATA_1)
    create_golongan_kata(
        data=CreateGolonganKata(
            id="NAMA",
            nama="kata nama",
            keterangan="kata yang digunakan untuk merujuk kepada benda.",
        )
    )
    konsep = create_konsep_by_annotated_text(annotated_text=data, lemma_name="ujian")
    assert konsep.keterangan == "Ini adalah konsep cubaan"
    assert konsep.cakupan[0].cakupan.nama == "tag 1"
    assert konsep.cakupan[1].cakupan.nama == "tag-2"


@mocks.bind_test_database
def test_create_konsep_attachment_with_error():
    data = AnnotatedText(body=DATA_1)
    create_golongan_kata(
        data=CreateGolonganKata(
            id="NAMA",
            nama="kata nama",
            keterangan="kata yang digunakan untuk merujuk kepada benda.",
        )
    )
    from samudra.models import Cakupan

    old_attr = Cakupan.connection_table
    try:
        delattr(Cakupan, "connection_table")
        with pytest.raises(AttributeError):
            create_konsep_by_annotated_text(annotated_text=data, lemma_name="ujian")
    finally:
        # Properly restore attr for other tests
        Cakupan.connection_table = old_attr


@mocks.bind_test_database
def test_get_minimum_lemma_info():
    data = AnnotatedText(body=DATA_1)
    create_golongan_kata(
        data=CreateGolonganKata(
            id="NAMA",
            nama="kata nama",
            keterangan="kata yang digunakan untuk merujuk kepada benda.",
        )
    )
    create_konsep_by_annotated_text(annotated_text=data, lemma_name="ujian")
    create_konsep_by_annotated_text(annotated_text=data, lemma_name="ujian")
    lemma = get_lemma_minimum_info(query=QueryFilter(limit=10))[0]
    assert lemma.nama == "ujian"
    assert lemma.id == 1
    assert len(lemma.konsep) == 2


@mocks.bind_test_database
def test_get_minimum_konsep_info():
    data = AnnotatedText(body=DATA_1)
    create_golongan_kata(
        data=CreateGolonganKata(
            id="NAMA",
            nama="kata nama",
            keterangan="kata yang digunakan untuk merujuk kepada benda.",
        )
    )
    create_konsep_by_annotated_text(annotated_text=data, lemma_name="ujian")
    konsep = get_konsep_minimum_info(where=None, limit=None)
    assert konsep == list(models.Konsep)


@mocks.bind_test_database
def test_get_cakupan_by_name():
    data = AnnotatedText(body=DATA_1)
    create_golongan_kata(
        data=CreateGolonganKata(
            id="NAMA",
            nama="kata nama",
            keterangan="kata yang digunakan untuk merujuk kepada benda.",
        )
    )
    create_konsep_by_annotated_text(annotated_text=data, lemma_name="ujian")
    cakupan = get_cakupan_by_name(nama="tag 1")
    assert cakupan[0].nama == "tag 1"


@mocks.bind_test_database
def test_get_kata_asing_by_name():
    data = AnnotatedText(body=DATA_1)
    create_golongan_kata(
        data=CreateGolonganKata(
            id="NAMA",
            nama="kata nama",
            keterangan="kata yang digunakan untuk merujuk kepada benda.",
        )
    )
    create_konsep_by_annotated_text(annotated_text=data, lemma_name="ujian")
    kata_asing = get_kata_asing_by_name(nama="concept")
    assert kata_asing[0].nama == "concept"
