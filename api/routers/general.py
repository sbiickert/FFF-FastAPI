from fastapi import APIRouter
from fastapi.responses import RedirectResponse

import api.schemas as fff_schema

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

@router.get("/transactiontypes/{category}", response_model=list[fff_schema.TransactionType])
def get_transaction_types(category: fff_schema.TransactionTypeCategory):
	return [fff_schema.TransactionType(id=1, name="Test", is_active=True, category=fff_schema.TransactionTypeCategory.expense, symbol="😇")]

