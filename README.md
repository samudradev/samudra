# Samudra

A simple dictionary web application.

## MVP Features

### Models

- Lemma (Lemma)
- Konsep (Concept)
- KataAsing (Foreign Word)
- Cakupan (Context of Meaning)

### Interactions

1. Add words with meaning. (DONE)
2. Add contexts to meaning. (DONE)
3. Add foreign words to meaning. (DONE)
4. Retrieve word and related information. (DONE)
5. Expose API using FastAPI. (DONE)

## Installation

1. Python 3.8 or later
2. Install [poetry](https://python-poetry.org/docs/)
3. `poetry install` (creating a virtual environment is recommended)

## Running the app

`python ./samudra/serve.py`

### Lemma

#### Create Lemma

Example using [httpie](www.httpie.io) and annotated post body

```shell
http POST :8000/lemma/{nama} body="sebahagian dari konsep #biasa #professional {lang.en:name} {lang.en:new} {meta.gol:nama}"
```

will create

```json
{
  "lemma": "{nama}",
  "konsep": {
    "keterangan": "sebahagian dari konsep",
    "golongan": "nama",
    "cakupan": [
      "biasa",
      "professional"
    ],
    "kata_asing": [
      {
        "bahasa": "en"
        "nama": "name"
      },
      {
        "bahasa": "en"
        "nama": "new"
      }
    ]
  }
}
```

## Ingin Menyumbang?

- Buat masa ini kami perlukan seseorang untuk membuat bahagian frontend.
  Sebolehnya, nak guna [Next.js](https://nextjs.org/).
- Boleh tambahbaik aplikasi dari segi pull request atau sekadar cadangan

Boleh hubungi saya melalui emel [makmal.thaza+samudra@gmail.com](mailto:makmal.thaza+samudra@gmail.com) atau di
Twitter [@Thaza_Kun](www.twitter.com/Thaza_Kun)