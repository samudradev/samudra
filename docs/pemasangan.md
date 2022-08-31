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

## Mulakan pelayan

Setelah selesai langkah pemasangan, mulakan pelayan menggunakan poetry
(poetry digunakan bagi memastikan arahan dalam fail python dilaksanakan
menggunakan keperluan yang sudah dijelaskan dalam fail `pyproject.toml`)

```shell
$ poetry run python ./samudra/serve.py
```

Jika anda menerima ralat mengenai ACCESS\_TOKEN\_EXPIRE\_MINUTES, ia adalah kerana environment variables tidak ditetapkan dengan betul. Masalah ini boleh dibetulkan dengan menetapkan environment variables yang betul semasa memulakan pelayan, contohnya:  

```shell
$ ACCESS_TOKEN_EXPIRE_MINUTES=60 poetry run python ./samudra/serve.py
```

