from dataclasses import dataclass

import pandas as pd
import peewee as pw

from samudra import schemas
from samudra.models import Lemma, Konsep, Cakupan, KataAsing

mock_db = pw.SqliteDatabase(':memory:')

models = [Lemma, Konsep, Cakupan, KataAsing]


def bind_test_database(function: callable, *args, **kwargs) -> callable:
    """Decorator to open and close a test database connection"""

    def wrapper():
        mock_db.bind(models)
        mock_db.create_tables(models)
        function(*args, **kwargs)
        mock_db.close()

    return wrapper


@dataclass
class TestLemma:
    nama = 'lemma ujian'
    konsep = dict(
        keterangan='Ini adalah lemma yang digunakan untuk ujian',
        golongan='kata nama',
        cakupan=[
            dict(
                nama='ujian',
                keterangan='lemma ini tidak wujud di luar ujian'
            )
        ],
        kata_asing=[
            dict(
                nama='test lemma',
                golongan='kata nama',
                bahasa='en'
            )
        ]
    )

    @property
    def to_schema(self) -> schemas.LemmaCreation:
        """Single boilerplate data for testing purposes"""
        return schemas.LemmaCreation(
            nama=self.nama,
            konsep=[
                schemas.KonsepCreation(
                    keterangan=self.konsep['keterangan'],
                    golongan=self.konsep['golongan'],
                    cakupan=[
                        schemas.CakupanCreation(
                            nama=cakupan.get('nama'),
                            keterangan=cakupan.get('keterangan'),
                        ) for cakupan in self.konsep['cakupan']
                    ],
                    kata_asing=[
                        schemas.KataAsingCreation(
                            nama=kata_asing.get('nama'),
                            golongan=kata_asing.get('golongan', self.konsep['golongan']),
                            bahasa=kata_asing.get('bahasa', 'en'),
                        ) for kata_asing in self.konsep['kata_asing']
                    ])
            ]
        )

    @property
    def from_excel(self) -> pd.DataFrame:
        """Mimics data from excel"""
        cakupan_list = ["ujian", "bukan betul"]
        kata_asing_list = ["test", "falsey"]
        indices = pd.MultiIndex.from_tuples([
            ("lemma", None),
            ("konsep", "keterangan"),
            ("konsep", "golongan"),
            ("konsep", "cakupan"),
            ("konsep", "kata_asing"),
        ])
        df = pd.DataFrame([
            [self.nama,
             self.konsep['keterangan'],
             self.konsep['golongan'],
             "|".join(cakupan_list),
             "|".join(kata_asing_list)],
        ],
            columns=indices
        )
        self.konsep['cakupan'] = [dict(nama=cakupan) for cakupan in cakupan_list]
        self.konsep['kata_asing'] = [dict(nama=kata_asing) for kata_asing in kata_asing_list]
        return df
