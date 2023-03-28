# Samudra

![test-badge](https://github.com/Thaza-Kun/samudra/actions/workflows/test.yml/badge.svg) ![docs-badge](https://github.com/Thaza-Kun/samudra/actions/workflows/docs.yml/badge.svg) ![black-badge](https://github.com/Thaza-Kun/samudra/actions/workflows/black.yml/badge.svg) ![pages-build-deployment-badge](https://github.com/Thaza-Kun/samudra/actions/workflows/pages/pages-build-deployment/badge.svg)

Sebuah aplikasi untuk memudahkan pencatatan istilah serta pengongsiannya sesama rakan sekerja atau orang awam.
Dengan memudahkan proses ini, kita dapat menambah jumlah rujukan bahasa Melayu dalam talian sekali gus mempercepatkan
perkembangannya dari segi penggunaan, penyelidikan serta pembelajarannya.

## Model

Model kamus direka supaya selari dengan padanan satu kata boleh mendukung banyak konsep
serta satu perkataan boleh dipadankan ke banyak kata asing yang bergantung pada konsep dan konteks yang digunakan.

![](./docs/img/model-samudra.png)

## Tentang Aplikasi

Pembangunan aplikasi ini ada dua arah:

1. [Samudra Sebagai Aplikasi Terminal](#Samudra-Sebagai-Aplikasi-Terminal)
2. [Samudra Sebagai Aplikasi Pelayan](#Samudra-Sebagai-Aplikasi-Pelayan)

> *warning*
> Buat masa ini pembangunan sedang ditumpukan pada arah 'Samudra Sebagai Aplikasi Terminal'.
> Maka, kefungsiannya sebagai satu pelayan dijangka rosak akibat perubahan kod teras.

### Prasyarat

1. [Python 3.8](https://www.python.org/) atau lebih tinggi
2. [Poetry](https://python-poetry.org/docs/) untuk pengurusan keperluan projek
3. [Git](https://git-scm.com/) untuk kawalan perubahan kod

### Pemasangan

1. Salin repositori ini guna git ke dalam folder bernama 'samudra'
    ```shell
   $ git clone https://github.com/Thaza-Kun/samudra.git samudra
   ```
2. Masuk ke dalam folder samudra
    ```shell
   $ cd samudra
   ```
3. Dapatkan semua keperluan projek menggunakan poetry
    ```shell
   $ poetry install
   ```

### Samudra Sebagai Aplikasi terminal

Tempat masuk aplikasi terminal diletakkan dalam `./samudra/main.py`.
Oleh itu, arahan di bawah akan berikan senarai arahan yang tersedia.

```shell
$ poetry run python ./samudra/main.py --help
```

### Samudra Sebagai Aplikasi Pelayan

#### Sediakan fail .env

Sebelum boleh memulakan pelayan, fail `.env` perlu wujud untuk menyediakan nilai yang berlainan bagi setiap salinan
aplikasi. Fail ini terletak dalam ROOT, iaitu tempat yang sama wujudnya `README.md` ini.
Biasanya, nilai-nilai yang diletakkan dalam ini adalah nilai-nilai rahsia yang tidak boleh dikomit masuk git.
Berikut merupakan nilai-nilai yang perlu ada dalam fail `.env` samudra:

```shell
# ./.env

# Buat masa sekarang ada tiga enjin: SQLite, MySQL, dan CockroachDB.
# SQLite sesuai untuk aplikasi lokal dan hanya satu pengguna.
# Yang lain memerlukan pelayan
ENGINE = SQLite

# Yang ini adalah nilai yang diperlukan untuk daftar masuk pelayan DB
# (Tidak perlu kalau pilih enjin SQLite)
DATABASE_USERNAME = 
DATABASE_PASSWORD = 

# Maklumat pelayan DB
# (Tidak perlu kalau pilih enjin SQLite)
DATABASE_NAME = 
DATABASE_HOST = 
DATABASE_PORT = 
DATABASE_OPTIONS = 

# Tempoh masa pengguna dibenarkan log masuk (dalam sukatan minit)
# (Wajib walaupun pilih enjin SQLite)
ACCESS_TOKEN_EXPIRE_MINUTES = 
```

#### Mulakan pelayan

Setelah selesai langkah pemasangan, mulakan pelayan menggunakan poetry
(poetry digunakan bagi memastikan arahan dalam fail python dilaksanakan
menggunakan keperluan yang sudah dijelaskan dalam fail `pyproject.toml`)

```shell
$ poetry run python ./samudra/serve.py
```

Jika anda menerima ralat mengenai nilai-nilai yang tidak tertakrif, rujuk bahagian [fail .env](#Sediakan fail .env).
Lihat sekiranya nilai-nilai yang tersenarai di situ sudah tertakrif belum.
Sekiranya nilai ralat itu tidak disenaraikan, boleh failkan isu.

### Penciptaan lemma / konsep

Bagi memudahkan penulisan konsep, samudra menggunakan pencatatan berconteng tapis contengan tersebut menjadi struktur
yang bermakna. Contengan perlu diletakkan di hujung keterangan kalau tidak, akan dihantar `SyntaxError` kerana ada lebih
dari satu kandungan teks.

- Contengan tagar `#` menandakan cakupan konsep tersebut. Misalnya, `#sains` menunjukkan konsep tersebut digunakan dalam
  sains. Boleh ada banyak tagar untuk setiap konsep.
- Contengan kurungan bertitik tindih `{kunci:nilai}` memadankan nilai pada kuncinya. Tanda titik `.` digunakan bagi
  meletakkan kata kunci dalam kata kunci. Buat masa ini, hanya kunci-kunci berikut yang diterima:
    - `{lang.en:nilai}` akan memadankan konsep ke kata asing berbahasa inggeris. Boleh padankan banyak kata asing ke
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

### Menyumbang kod

1. Buat cabang baharu agar setiap perubahan tersebut tidak mengganggu cabang utama. Namakan cabang secara deskriptif (
   seperti menamakan ciri yang ingin ditambah).
    ```shell
   $ git checkout -b nama_cabang
   ```
2. Buat perubahan yang diinginkan. Pastikan `git commit -m "ringkaskan perubahan di sini"` untuk simpan perubahan.
3. Hantar cabang perubahan ke repo github. Gunakan `nama_cabang` yang sama dengan langkah pertama.
    ```shell
   $ git push --set-upstream origin nama_cabang
   ```
4. Hantar _pull request_ dan jelaskan perubahan yang telah dilakukan.

## Ingin Menyumbang?

- Bahagian frontent boleh ke repo [alserembani94/laman-samudra](https://github.com/alserembani94/laman-samudra/).
  Terima kasih @alserembani94 kerana sudi menggerakkan bahagian laman!
- Boleh tambahbaik aplikasi dari segi _pull request_ (ikut arahan di bahagian [# Menyumbang Kod](#menyumbang-kod)) atau
  sekadar cadangan
- Boleh sumbangkan secangkir kopi di [Ko-fi](https://ko-fi.com/thaza_kun)

Boleh hubungi saya melalui emel [makmal.thaza+samudra@gmail.com](mailto:makmal.thaza+samudra@gmail.com) atau di
Twitter [@Thaza_Kun](www.twitter.com/Thaza_Kun).
