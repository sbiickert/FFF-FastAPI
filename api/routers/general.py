from fastapi import APIRouter

import api.schemas as fff_schema

router = APIRouter()

# FFF6 Symfony (php bin/console debug:router)
# get_root                     GET|HEAD   ANY      ANY    /                                        
# app_heartbeat_get            GET|HEAD   ANY      ANY    /heartbeat                               
# get_transaction_types        GET|HEAD   ANY      ANY    /transactiontypes/{category}.{_format}   
 
@router.get("/")
async def get_root():
	pass

@router.get("heartbeat")
async def get_heartbeat():
	pass

@router.get("/transactiontypes/{category}", response_model=list[fff_schema.TransactionType])
def get_transaction_types(category: fff_schema.TransactionTypeCategory):
	return [fff_schema.TransactionType(id=1, name="Test", is_active=True, category=fff_schema.TransactionTypeCategory.expense, symbol="😇")]

