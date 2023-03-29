# Samudra

![test-badge](https://github.com/Thaza-Kun/samudra/actions/workflows/test.yml/badge.svg) ![docs-badge](https://github.com/Thaza-Kun/samudra/actions/workflows/docs.yml/badge.svg) ![black-badge](https://github.com/Thaza-Kun/samudra/actions/workflows/black.yml/badge.svg) ![pages-build-deployment-badge](https://github.com/Thaza-Kun/samudra/actions/workflows/pages/pages-build-deployment/badge.svg)

> *info*
> Repositori ini sudah dikhaskan sebagai sebuah modul teras samudra sejak v0.9.1. 
> Mod pelayan dan mod terminal sudah dimansuhkan dari repo ini. 
> Antaramuka bergrafik sedang diusahakan sebagai repo asing di https://github.com/samudradev/samudra-gui. Rujuk https://github.com/samudradev/samudra/releases/tag/v0.9.1

Sebuah aplikasi untuk memudahkan pencatatan istilah serta pengongsiannya sesama rakan sekerja atau orang awam.
Dengan memudahkan proses ini, kita dapat menambah jumlah rujukan bahasa Melayu dalam talian sekali gus mempercepatkan
perkembangannya dari segi penggunaan, penyelidikan serta pembelajarannya.

## Model

Model kamus direka supaya selari dengan padanan satu kata boleh mendukung banyak konsep
serta satu perkataan boleh dipadankan ke banyak kata asing yang bergantung pada konsep dan konteks yang digunakan.

![](./docs/img/model-samudra.png)

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
