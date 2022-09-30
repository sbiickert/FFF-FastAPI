from fastapi import APIRouter, status, Query, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

import api.schemas as fff_schema
import api.cruds.transactions as fff_crud
from api.db import get_db

router = APIRouter()
      

# .d8888. d888888b d8b   db  d888b  db      d88888b    d888b  d88888b d888888b 
# 88'  YP   `88'   888o  88 88' Y8b 88      88'       88' Y8b 88'     `~~88~~' 
# `8bo.      88    88V8o 88 88      88      88ooooo   88      88ooooo    88    
#   `Y8b.    88    88 V8o88 88  ooo 88      88~~~~~   88  ooo 88~~~~~    88    
# db   8D   .88.   88  V888 88. ~8~ 88booo. 88.       88. ~8~ 88.        88    
# `8888Y' Y888888P VP   V8P  Y888P  Y88888P Y88888P    Y888P  Y88888P    YP    
                                                                             
                                                                             
@router.get("/transaction/{id}", response_model=fff_schema.TransactionOut)
async def get_transaction(id: int, db: AsyncSession = Depends(get_db)):
	t = await fff_crud.get_transaction(id, db)
	if t is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{id} is not a valid transaction id")
	return t

# .d8888. d888888b d8b   db  d888b  db      d88888b   d88888b d8888b. d888888b d888888b 
# 88'  YP   `88'   888o  88 88' Y8b 88      88'       88'     88  `8D   `88'   `~~88~~' 
# `8bo.      88    88V8o 88 88      88      88ooooo   88ooooo 88   88    88       88    
#   `Y8b.    88    88 V8o88 88  ooo 88      88~~~~~   88~~~~~ 88   88    88       88    
# db   8D   .88.   88  V888 88. ~8~ 88booo. 88.       88.     88  .8D   .88.      88    
# `8888Y' Y888888P VP   V8P  Y888P  Y88888P Y88888P   Y88888P Y8888D' Y888888P    YP    
                                                                                                                                                                 
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


# .88b  d88. db    db db      d888888b d888888b         d888b  d88888b d888888b 
# 88'YbdP`88 88    88 88      `~~88~~'   `88'          88' Y8b 88'     `~~88~~' 
# 88  88  88 88    88 88         88       88           88      88ooooo    88    
# 88  88  88 88    88 88         88       88    C8888D 88  ooo 88~~~~~    88    
# 88  88  88 88b  d88 88booo.    88      .88.          88. ~8~ 88.        88    
# YP  YP  YP ~Y8888P' Y88888P    YP    Y888888P         Y888P  Y88888P    YP    

@router.get("/transactions", response_model=list[fff_schema.TransactionOut])
async def get_transactions_with_ids(tids: str = Query(default="", regex="^[,\d]+$"),
									db: AsyncSession = Depends(get_db)):
	id_list = list(map(int, filter(None, tids.split(","))))
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


# .88b  d88. db    db db      d888888b d888888b        d88888b d8888b. d888888b d888888b 
# 88'YbdP`88 88    88 88      `~~88~~'   `88'          88'     88  `8D   `88'   `~~88~~' 
# 88  88  88 88    88 88         88       88           88ooooo 88   88    88       88    
# 88  88  88 88    88 88         88       88    C8888D 88~~~~~ 88   88    88       88    
# 88  88  88 88b  d88 88booo.    88      .88.          88.     88  .8D   .88.      88    
# YP  YP  YP ~Y8888P' Y88888P    YP    Y888888P        Y88888P Y8888D' Y888888P    YP    

@router.post("/transactions", response_model=list[fff_schema.TransactionOut], status_code=status.HTTP_201_CREATED)
async def post_transactions(t_items: list[fff_schema.TransactionIn], db: AsyncSession = Depends(get_db)):
	return await fff_crud.create_transactions(t_items, db)

@router.put("/transactions", response_model=list[fff_schema.TransactionOut])
async def put_transactions(t_items: list[fff_schema.TransactionInWithID], db: AsyncSession = Depends(get_db)):
	t_ids = []
	for t_item in t_items:
		t_ids.append(t_item.id)
	originals = await fff_crud.get_transactions(t_ids, db)
	return await fff_crud.update_transactions(originals, t_items, db)

@router.delete("/transactions",  response_model=fff_schema.TransactionsMessage)
async def delete_transactions(tids: str = Query(default="", regex="^[,\d]+$"), db: AsyncSession = Depends(get_db)):
	id_list = list(map(int, filter(None, tids.split(","))))
	transactions = await fff_crud.get_transactions(id_list, db)
	deleted_ids = await fff_crud.delete_transactions(originals=transactions, db=db)
	print(deleted_ids)
	return fff_schema.TransactionsMessage(message="Deleted transactions", tids=deleted_ids)
