from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from passlib.context import CryptContext

from datetime import datetime, timedelta

import api.schemas as fff_schema
import api.cruds.other as fff_crud
from api.db import get_db

# from random.org
SALT="B2jE2Lh9z1E7GQj7j5C1sb"
# openssl rand -hex 32
SECRET_KEY = "febeab36aaf79f36c2bf8ec33c7234a2105b98e14d3cc8197cacf1aa0aff1d03"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password, salt=SALT)


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
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
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

