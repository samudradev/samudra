from typing import Optional
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from samudra import models, schemas
from samudra.core import auth
from samudra.server.dependencies import get_db
from datetime import datetime, timedelta

from pydantic import BaseModel

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


class PenggunaCreateDTO(BaseModel):
    nama: str
    katalaluan: str


def create_access_token(data: dict, expires_delta: Optional[timedelta]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt


router = APIRouter(prefix="/authentication", dependencies=[Depends(get_db)])


@router.post("/daftar", response_model=schemas.DaftarResponse)
def create_pengguna(pengguna: PenggunaCreateDTO):
    try:
        pengguna = auth.get_pengguna_by_nama(pengguna.nama)
        raise HTTPException(status_code=409, detail="User already exist")
    except models.Pengguna.DoesNotExist:
        pengguna = auth.create_pengguna(
            nama=pengguna.nama, katalaluan=pengguna.katalaluan
        )
        return {
            "pengguna": pengguna.nama,
            "mesej": f"Pengguna {pengguna.nama} telah berjaya didaftarkan!",
        }
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=e.msg)


@router.post("/logmasuk", response_model=schemas.LogMasukResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        pengguna = auth.authenticate_pengguna(form_data.username, form_data.password)
        if not pengguna:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": pengguna.nama}, expires_delta=access_token_expires
        )
        return {
            "pengguna": form_data.username,
            "token": {"access_token": access_token, "token_type": "bearer"},
        }
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=e.msg)
