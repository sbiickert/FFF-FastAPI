from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas as fff_schema
import api.cruds.other as fff_crud
from api.db import get_db
from api.security import get_current_user, fake_hash_password

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

@router.get("/users/me", response_model=fff_schema.UserOut)
async def get_user(current_user: fff_schema.UserOut = Depends(get_current_user)):
	return current_user

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
	user = await fff_crud.get_user(form_data.username, db)
	if user is None:
		print(f"no such user {form_data.username}")
		raise HTTPException(status_code=400, detail="Incorrect username or password")
	hashed_password = fake_hash_password(form_data.password)
	if not hashed_password == user.password:
		print(f"hashed password didn't match")
		raise HTTPException(status_code=400, detail="Incorrect username or password")

	return {"access_token": user.email, "token_type": "bearer"}