from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from samudra import models, schemas
from samudra.core import auth
from samudra.server.dependencies import get_db
from datetime import timedelta

from samudra.server.tokens import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    PenggunaCreateDTO,
    create_access_token,
)

# TODO Set peranan
router = APIRouter(prefix="/auth", dependencies=[Depends(get_db)])


@router.post("/daftar", response_model=schemas.DaftarResponse)
def create_pengguna(pengguna: PenggunaCreateDTO):
    """POST `/auth/daftar`. Register user

    Args:
        pengguna (PenggunaCreateDTO): User

    Raises:
        HTTPException: 409 Exception. User already exist
        HTTPException: 400 Bad Request Exception.

    Returns:
        [`schemas.DaftarResponse`][samudra.schemas.tables.user.DaftarResponse]
    """
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
async def login_pengguna(form_data: OAuth2PasswordRequestForm = Depends()):
    """POST `/auth/logmasuk`. Log in.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): username and password. Defaults to Depends().

    Raises:
        HTTPException: 401 Unauthorized Exception. Incorrect username or password.
        HTTPException: 400 Bad Request Exception.

    Returns:
        [`schemas.LogMasukResponse`][samudra.schemas.tables.user.LogMasukResponse]
    """
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
