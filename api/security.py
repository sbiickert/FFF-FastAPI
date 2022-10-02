from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas as fff_schema
import api.cruds.other as fff_crud
from api.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token: str, db: AsyncSession = Depends(get_db)) -> fff_schema.UserOut | None:
	return fff_crud.get_user_for_token(token, db)


def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_current_user(token: str = Depends(oauth2_scheme)) -> fff_schema.UserOut:
    user = fake_decode_token(token)
    return user

