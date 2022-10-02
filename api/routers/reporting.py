from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import re

import api.schemas as fff_schema
import api.cruds.other as fff_crud
from api.db import get_db
from api.security import oauth2_scheme

router = APIRouter()

# FFF6 Symfony (php bin/console debug:router)
# balance                      GET|HEAD   ANY      ANY    /balance/{y}/{m}/{d}/{_format}           
# search                       GET|HEAD   ANY      ANY    /search/{_format}                        
# summary                      GET|HEAD   ANY      ANY    /summary/{y}/{m}/{_format}               

@router.get("/search", response_model=list[fff_schema.TransactionOut])
async def get_search(q: str, db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
	clean_q = re.sub("[^\w %]", "", q)
	return await fff_crud.search_transactions(f"%{clean_q}%", db)

@router.get("/balance/{year}/{month}/{day}")
async def get_balance(year: int, month: int = -1, day: int = -1):
	pass

@router.get("/summary/{year}/{month}")
async def get_summary(year: int, month: int = -1):
	pass
