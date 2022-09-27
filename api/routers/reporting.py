from fastapi import APIRouter

import api.schemas as fff_schema

router = APIRouter()

# FFF6 Symfony (php bin/console debug:router)
# balance                      GET|HEAD   ANY      ANY    /balance/{y}/{m}/{d}/{_format}           
# search                       GET|HEAD   ANY      ANY    /search/{_format}                        
# summary                      GET|HEAD   ANY      ANY    /summary/{y}/{m}/{_format}               

@router.get("/search", response_model=list[fff_schema.TransactionOut])
def get_search(q: str):
	pass

@router.get("/balance/{year}/{month}/{day}")
def get_balance(year: int, month: int = -1, day: int = -1):
	pass

@router.get("/summary/{year}/{month}")
def get_summary(year: int, month: int = -1):
	pass
