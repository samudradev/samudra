from typing import List, Union, Optional, Dict, Any
import os
import pydantic
from fastapi import APIRouter, Depends, HTTPException, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from samudra import models, schemas
from samudra.core import auth
from samudra.models.user import User
from samudra.server.dependencies import get_db
from samudra.schemas.tables._helper import PeeweeGetterDict, ORMSchema
from datetime import datetime, timedelta

from pydantic import BaseModel

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

class UserCreateDTO(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: Optional[timedelta]):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter(
    prefix="/authentication",
    dependencies=[Depends(get_db)]
)

@router.post('/daftar', response_model=schemas.DaftarResponse)
def create_user(user: UserCreateDTO):
    try:
        user = auth.get_user_by_username(user.username)
        raise HTTPException(status_code=409, detail='User already exist')
    except models.User.DoesNotExist:
        user = auth.create_user(username=user.username, password=user.password)
        return {
            "pengguna": user.username,
            "mesej": f'Pengguna {user.username} telah berjaya didaftarkan!'
        }
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=e.msg)


@router.post('/logmasuk', response_model=schemas.LogMasukResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = auth.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {
            "pengguna": form_data.username,
            "token": {
                "access_token": access_token,
                "token_type": "bearer"
            }
        }
    except SyntaxError as e:
        raise HTTPException(status_code=400, detail=e.msg)
