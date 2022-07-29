# Samudra

Sebuah aplikasi untuk memudahkan pencatatan istilah serta pengongsiannya sesama rakan sekerja atau orang awam.
Dengan memudahkan proses ini, kita dapat menambah jumlah rujukan bahasa Melayu dalam talian sekali gus mempercepatkan
perkembangannya dari segi penggunaan, penyelidikan serta pembelajarannya.

## Model

Model kamus direka supaya selari dengan padanan satu kata boleh mendukung banyak konsep
serta satu perkataan boleh dipadankan ke banyak kata asing yang bergantung pada konsep dan konteks yang digunakan.

![](./docs/img/model-samudra.png)

## Tentang Aplikasi

### Pemasangan

1. Python 3.8 atau lebih
2. Guna [poetry](https://python-poetry.org/docs/) (digalakkan)
3. `poetry install`

### Mulakan pelayan

`python ./samudra/serve.py`

### Penciptaan lemma

Ini adalah contoh menggunakan [httpie](www.httpie.io).

```shell
http POST :8000/lemma/nama body="keterangan konsep #pasar #percakapan {lang.en:name} {lang.en:new} {meta.gol:NAMA}"
```

akan menghasilkan

```json
{
  "lemma": "nama",
  "konsep": {
    "keterangan": "keterangan konsep",
    "golongan": "NAMA",
    "cakupan": [
      "pasar",
      "percakapan"
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
- Boleh sumbangkan secangkir kopi di [Ko-fi](https://ko-fi.com/thaza_kun)

Boleh hubungi saya melalui emel [makmal.thaza+samudra@gmail.com](mailto:makmal.thaza+samudra@gmail.com) atau di
Twitter [@Thaza_Kun](www.twitter.com/Thaza_Kun).