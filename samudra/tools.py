import os
from typing import List

import pandas as pd

from samudra import models, schemas, crud


def datapath(filename: str) -> str:
    return os.path.join(os.getcwd(), 'data', filename)


def split_text(text: str, delimiter: str) -> List[str]:
    return text.split(delimiter)


def parse_dataframe(dataframe: pd.DataFrame, list_delimiter: str = '|') -> List[schemas.LemmaCreation]:
    # TODO: Split the word for cakupan and kata_asing
    schema_list = []
    for lemma, konsep in zip(
            dataframe['lemma'].to_dict(orient='list').values(),
            dataframe['konsep'].to_dict(orient='records')):
        schema_list.append(schemas.LemmaCreation(
            nama=lemma[0],
            konsep=[
                schemas.KonsepCreation(
                    golongan=konsep['golongan'],
                    keterangan=konsep['keterangan'],
                    cakupan=[schemas.CakupanCreation(nama=cakupan) for cakupan in
                             split_text(konsep['cakupan'], delimiter=list_delimiter)],
                    kata_asing=[
                        schemas.KataAsingCreation(nama=kata, golongan=konsep['golongan'], bahasa='en') for
                        kata in split_text(konsep['kata_asing'], delimiter=list_delimiter)]
                )
            ]
        ))
    return schema_list


def read_excel(filename: str, list_delimiter: str = '|') -> List[schemas.LemmaCreation]:
    df = pd.read_excel(datapath(filename), header=[0, 1])
    return parse_dataframe(dataframe=df, list_delimiter=list_delimiter)


def excel_to_sql(filename: str, list_delimiter: str = '|') -> List[models.Lemma]:
    data = read_excel(filename=filename, list_delimiter=list_delimiter)
    return [crud.create_lemma(lemma) for lemma in data]
