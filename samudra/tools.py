import os
from typing import List, Dict

import pandas as pd

from samudra import models, schemas, crud


def datapath(filename: str) -> str:
    return os.path.join(os.getcwd(), 'data', filename)


def list_of_dicts_from_string(string: str, key: str, delimiter: str = '|') -> List[Dict[str, str]]:
    list_of_strings = string.split(delimiter)
    ret = []
    for single_string in list_of_strings:
        ret.append({key: single_string})
    return ret


def read_csv(filename: str, delimiter: str = ',', bahasa_kata_asing: str = 'en') -> List[schemas.LemmaCreation]:
    df = pd.read_csv(datapath(filename), delimiter=delimiter)
    df['cakupan'] = df['cakupan'].str.split('|')
    df["kata_asing"] = df["kata_asing"].str.split('|')
    return [
        schemas.LemmaCreation(
            nama=row['lemma'],
            konsep=[
                schemas.KonsepCreation(
                    golongan=row['golongan'],
                    keterangan=row['keterangan'],
                    cakupan=[schemas.CakupanCreation(nama=cakupan) for cakupan in row['cakupan']],
                    kata_asing=[
                        schemas.KataAsingCreation(nama=kata, golongan=row['golongan'], bahasa=bahasa_kata_asing) for
                        kata in row['kata_asing']]
                )
            ]
        ) for row in df.to_dict(orient='records')
    ]


def csv_to_sql(filename: str, delimiter: str = ',', preserve_csv_data: bool = False) -> List[models.Lemma]:
    data: List[schemas.LemmaCreation] = read_csv(filename, delimiter)
    if not preserve_csv_data:
        columnnames = ['lemma', 'golongan', 'keterangan', 'cakupan', 'kata_asing']
        pd.DataFrame(
            None,
            columns=columnnames
        ).to_csv(datapath(filename))
    return [crud.create_lemma(lemma) for lemma in data]
