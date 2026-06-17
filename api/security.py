from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
import os
from datetime import datetime, timedelta, timezone

import api.schemas as fff_schema
import api.cruds.other as fff_crud
from api.db import get_db

# openssl rand -hex 32
SECRET_KEY = "febeab36aaf79f36c2bf8ec33c7234a2105b98e14d3cc8197cacf1aa0aff1d03"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

import bcrypt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


async def authenticate_user(email: str, password: str, db: AsyncSession = Depends(get_db)) -> fff_schema.UserOut | None:
    user = await fff_crud.get_user(email, db)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> fff_schema.UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = fff_schema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await fff_crud.get_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_group(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> fff_schema.UserGroup:
    user = await get_current_user(token, db)
    return await fff_crud.get_user_group(user.user_group_id, db)
