from samudra import models, schemas


def create_golongan_kata(data: schemas.CreateGolonganKata) -> models.GolonganKata:
    return models.GolonganKata.create(id=data.id, nama=data.nama, keterangan=data.keterangan)
