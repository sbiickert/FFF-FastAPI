import importlib
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from datetime import timedelta

import api.schemas as fff_schema
import api.cruds.other as fff_crud
from api.db import get_db
from api.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user, authenticate_user, get_password_hash, verify_password

router = APIRouter()

 
@router.get("/")
async def get_root(request: Request):
	return RedirectResponse(request.scope.get('root_path', '') + '/docs')
	#return {"message": "Welcome to the FFF version 6"}

@router.get("/heartbeat")
async def get_heartbeat(current_user: fff_schema.UserOut = Depends(get_current_user)):
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
	user = await authenticate_user(form_data.username, form_data.password, db)
	if user is None:
		raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
	access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	access_token = create_access_token(
		data={"sub": user.email}, expires_delta=access_token_expires
	)
	return {"access_token": access_token, "token_type": "bearer"}

@router.put("/users/me/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
	payload: fff_schema.PasswordChange,
	current_user: fff_schema.UserOut = Depends(get_current_user),
	db: AsyncSession = Depends(get_db),
):
	db_user = await fff_crud.get_user(current_user.email, db)
	if not verify_password(payload.current_password, db_user.password):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Current password is incorrect")
	await fff_crud.update_user_password(current_user.id, get_password_hash(payload.new_password), db)

@router.get("/hasher")
async def hash_string(input: str) -> str:
	return get_password_hash(input)