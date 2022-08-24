# Model Samudra

Sebuah `model` samudra merujuk kepada objek atau `class` yang dipadankan dengan jadual dalam pangkalan data.
Pemadanan dan interaksi dengan pangkalan data diuruskan oleh
pakej [peewee](http://docs.peewee-orm.com/en/latest/index.html) dan berperanan mentakrifkan bentuk data serta hubungkait
sesama data.

Setiap model tersimpan dalam direktori `samudra/models` dan mewarisi `BaseModel` yang mempunyai dua medan asasi: `id`
dan `tarikh_masuk`. Pengembangan dan perkemasan model sedang dijalankan di
cabang [`expand-model`](https://github.com/Thaza-Kun/samudra/tree/expand-model/samudra).

## Data Kamus

### Model Utama

Buat masa ini terdapat 4 model yang berfungsi memegang data kata-kata:

1. Lemma
2. Konsep
3. Cakupan
4. KataAsing

Hubungkait antara setiap model digambarkan sebegini:

![](img/model-samudra.png)

### Model Pengantara

Model `Cakupan` dan `KataAsing` bersambungan dengan `Konsep` secara padanan banyak kepada banyak.
Oleh itu, perlunya ada model pengantara yang memegang data perhubungan tersebut:

1. CakupanXKonsep
2. KataAsingXKonsep