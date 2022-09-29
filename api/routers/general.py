from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas as fff_schema
import api.cruds.other as fff_crud
from api.db import get_db

router = APIRouter()

# FFF6 Symfony (php bin/console debug:router)
# get_root                     GET|HEAD   ANY      ANY    /                                        
# app_heartbeat_get            GET|HEAD   ANY      ANY    /heartbeat                               
# get_transaction_types        GET|HEAD   ANY      ANY    /transactiontypes/{category}.{_format}   
 
@router.get("/")
async def get_root():
	return RedirectResponse('/docs')
	#return {"message": "Welcome to the FFF version 6"}

@router.get("heartbeat")
async def get_heartbeat():
	return {"message": "Welcome to the FFF version 6"}

@router.get("/transactiontype/{id}", response_model=fff_schema.TransactionType)
async def get_transaction_type(id: int, db: AsyncSession = Depends(get_db)):
	tt = await fff_crud.get_transaction_type(id, db)
	if tt is None:
		raise HTTPException(status.HTTP_404_NOT_FOUND, "No such transaction type.")
	return tt

@router.get("/transactiontypes/{category}", response_model=list[fff_schema.TransactionType])
async def get_transaction_types(category: fff_schema.TransactionTypeCategory, db: AsyncSession = Depends(get_db)):
	return await fff_crud.get_transaction_types(category, db)

