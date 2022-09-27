# Pemasangan

## Prasyarat

1. [Python 3.8](https://www.python.org/) atau lebih tinggi
2. [Poetry](https://python-poetry.org/docs/) untuk pengurusan keperluan projek
3. [Git](https://git-scm.com/) untuk kawalan perubahan kod

## Pemasangan

```shell
# 1. Salin repositori ini guna git ke dalam folder bernama 'samudra'
$ git clone https://github.com/Thaza-Kun/samudra.git samudra

# 2. Masuk ke dalam folder samudra
$ cd samudra

# 3. Dapatkan semua keperluan projek menggunakan poetry
$ poetry install
```

### Sediakan fail .env

Sebelum boleh memulakan pelayan, fail `.env` perlu wujud untuk menyediakan nilai yang berlainan bagi setiap salinan
aplikasi. Fail ini terletak dalam ROOT, iaitu tempat yang sama wujudnya `pyproject.toml`.
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

### Mulakan pelayan

Setelah selesai langkah pemasangan, mulakan pelayan menggunakan poetry
(poetry digunakan bagi memastikan arahan dalam fail python dilaksanakan
menggunakan keperluan yang sudah dijelaskan dalam fail `pyproject.toml`)

```shell
$ poetry run python ./samudra/serve.py
```

Jika anda menerima ralat mengenai nilai-nilai yang tidak tertakrif, rujuk bahagian [fail .env](#Sediakan fail .env).
Lihat sekiranya nilai-nilai yang tersenarai di situ sudah tertakrif belum.
Sekiranya nilai ralat itu tidak disenaraikan, boleh failkan isu.

