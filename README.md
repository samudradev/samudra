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

`poetry run python ./samudra/serve.py`

## Penciptaan lemma / konsep

Bagi memudahkan penulisan konsep, samudra menggunakan pencatatan berconteng tapis contengan tersebut menjadi struktur
yang bermakna. Contengan perlu diletakkan di hujung keterangan kalau tidak, akan dihantar `SyntaxError` kerana ada lebih
dari satu kandungan teks.

- Contengan tagar `#` menandakan cakupan konsep tersebut. Misalnya, `#sains` menunjukkan konsep tersebut digunakan dalam
  sains. Boleh ada banyak tagar untuk setiap konsep.
- Contengan kurungan bertitik tindih `{kunci:nilai}` memadankan nilai pada kuncinya. Tanda titik `.` digunakan bagi
  meletakkan kata kunci dalam kata kunci. Buat masa ini, hanya kunci-kunci berikut yang diterima:
    - `{lang:en:nilai}` akan memadankan konsep ke kata asing berbahasa inggeris. Boleh padankan banyak kata asing ke
      satu konsep. Kata asing berbahasa lain masih sedang diusahakan.
    - `{terj.en:nilai}` (kependekan untuk 'terjemah') akan buat benda sama dengan `{lang.en:nilai}` (boleh bercampur).
    - `{meta.gol:NAMA}` akan meletakkan penggolongan kata pada konsep tersebut. Ini adalah nilai wajib dan hanya satu
      golongan untuk setiap konsep.

Ini adalah contoh menggunakan [httpie](www.httpie.io).

```shell
http POST :8000/lemma/nama body="keterangan konsep #pasar #percakapan {terj.en:name} {lang.en:new} {meta.gol:NAMA}"
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
        "bahasa": "en",
        "nama": "name"
      },
      {
        "bahasa": "en",
        "nama": "new"
      }
    ]
  }
}
```

## Ingin Menyumbang?

- Bahagian frontent boleh ke repo [alserembani94/laman-samudra](https://github.com/alserembani94/laman-samudra/).
  Terima kasih @alserembani94 kerana sudi menggerakkan bahagian laman!
- Boleh tambahbaik aplikasi dari segi pull request atau sekadar cadangan
- Boleh sumbangkan secangkir kopi di [Ko-fi](https://ko-fi.com/thaza_kun)

Boleh hubungi saya melalui emel [makmal.thaza+samudra@gmail.com](mailto:makmal.thaza+samudra@gmail.com) atau di
Twitter [@Thaza_Kun](www.twitter.com/Thaza_Kun).
