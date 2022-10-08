from fastapi import APIRouter, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import re

import api.schemas as fff_schema
import api.cruds.other as fff_crud
from api.db import get_db
from api.security import get_current_user_group

router = APIRouter()

# FFF6 Symfony (php bin/console debug:router)
# balance                      GET|HEAD   ANY      ANY    /balance/{y}/{m}/{d}/{_format}           
# search                       GET|HEAD   ANY      ANY    /search/{_format}                        
# summary                      GET|HEAD   ANY      ANY    /summary/{y}/{m}/{_format}               

@router.get("/search", response_model=list[fff_schema.TransactionOut])
async def get_search(q: str, db: AsyncSession = Depends(get_db), 
					current_user_group: fff_schema.UserGroup = Depends(get_current_user_group)):
	clean_q = re.sub("[^\w %]", "", q)
	return await fff_crud.search_transactions(f"%{clean_q}%", current_user_group, db)

@router.get("/balance/{year}/{month}/{day}")
async def get_balance(year: int = Path(ge=2000, le=2070),
					month: int = Path(le=12, default=-1), 
					day: int = Path(le=31, default=-1), 
					db: AsyncSession = Depends(get_db), 
					current_user_group: fff_schema.UserGroup = Depends(get_current_user_group)):
	if month < 1:
		return await fff_crud.get_balance_for_year(year, current_user_group, db)
	if day < 1:
		return await fff_crud.get_balance_for_month(year, month, current_user_group, db)
	return await fff_crud.get_balance_for_date(year, month, day, current_user_group, db)

@router.get("/summary/{year}/{month}")
async def get_summary(year: int, month: int = -1,
					db: AsyncSession = Depends(get_db), 
					current_user_group: fff_schema.UserGroup = Depends(get_current_user_group)):
	return await fff_crud.get_summary_for_month(year, month, current_user_group, db)
