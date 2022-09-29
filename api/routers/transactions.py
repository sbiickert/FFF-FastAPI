from email.policy import default
from fastapi import APIRouter, status, Query, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

import api.schemas as fff_schema
import api.cruds.transactions as fff_crud
from api.db import get_db

router = APIRouter()

# FFF6 Symfony (php bin/console debug:router)
# get_transaction              GET|HEAD   ANY      ANY    /transaction/{id}.{_format}              
# post_transaction             POST       ANY      ANY    /transaction                             
# put_transaction              PUT        ANY      ANY    /transaction/{id}                        
# delete_transaction           DELETE     ANY      ANY    /transaction/{id}                        
# get_transactions_for_date    GET|HEAD   ANY      ANY    /transactions/{y}/{m}/{d}/{_format}      
# get_transactions_with_ids    GET|HEAD   ANY      ANY    /transactions/{_format}                  
# get_transactions_in_series   GET|HEAD   ANY      ANY    /transactions/series/{series}.{_format}  
# post_transactions            POST       ANY      ANY    /transactions                            
# put_transactions             PUT        ANY      ANY    /transactions                            
# delete_transactions          DELETE     ANY      ANY    /transactions                            

@router.get("/transaction/{id}", response_model=fff_schema.TransactionOut)
async def get_transaction(id: int, db: AsyncSession = Depends(get_db)):
	t = await fff_crud.get_transaction(id, db)
	if t is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{id} is not a valid transaction id")
	return t

@router.post("/transaction", response_model=fff_schema.TransactionOut, status_code=status.HTTP_201_CREATED)
async def post_transaction(t_item: fff_schema.TransactionIn, db: AsyncSession = Depends(get_db)):
	return await fff_crud.create_transaction(t_item, db)

@router.put("/transaction/{id}", response_model=fff_schema.TransactionOut)
async def put_transaction(id: int, t_item: fff_schema.TransactionIn, db: AsyncSession = Depends(get_db)):
	t = await fff_crud.get_transaction(id, db)
	if t is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{id} is not a valid transaction id")
	return await fff_crud.update_transaction(original=t, updated_t=t_item, db=db)

@router.delete("/transaction/{id}", response_model=fff_schema.TransactionsMessage)
async def delete_transaction(id: int, db: AsyncSession = Depends(get_db)):
	t = await fff_crud.get_transaction(id, db)
	if t is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{id} is not a valid transaction id")
	await fff_crud.delete_transaction(original=t, db=db)
	return fff_schema.TransactionsMessage(message="Deleted transaction", tids=[id])



@router.get("/transactions", response_model=list[fff_schema.TransactionOut])
async def get_transactions_with_ids(tids: str = Query(default="", regex="^[,\d]+$"),
									db: AsyncSession = Depends(get_db)):
	id_list = list(map(int, tids.split(",")))
	return await fff_crud.get_transactions(ids=id_list, db=db)

@router.get("/transactions/series/{series}", response_model=list[fff_schema.TransactionOut])
async def get_transactions_in_series(series: UUID, db: AsyncSession = Depends(get_db)):
	return await fff_crud.get_transactions_in_series(series, db)

@router.get("/transactions/{year}/{month}/{day}", response_model=list[fff_schema.TransactionOut])
async def get_transactions_for(year: int = Path(ge=2000, le=2070),
								month: int = Path(ge=1, le=12), 
								day: int = Path(le=31, default=-1),
								tt: int = -1,
								c: fff_schema.TransactionTypeCategory = fff_schema.TransactionTypeCategory.all,
								db: AsyncSession = Depends(get_db)):
	if day < 1:
		# Between the first and last of the month
		return await fff_crud.get_transactions_for_month(year, month, c, tt, db)
	# else on a specific day
	return await fff_crud.get_transactions_for_date(year, month, day, c, tt, db)



@router.post("/transactions", response_model=list[fff_schema.TransactionOut], status_code=status.HTTP_201_CREATED)
def post_transactions():
	pass

@router.put("/transactions", response_model=list[fff_schema.TransactionOut])
def put_transactions():
	pass

@router.delete("/transactions",  response_model=fff_schema.TransactionsMessage)
def delete_transactions(tids: str = Query(default="", regex="^[,\d]+$")):
	id_list = list(map(int, tids.split(",")))
	return fff_schema.TransactionsMessage(message="Deleted transactions", tids=id_list)
