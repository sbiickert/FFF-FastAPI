from fastapi import APIRouter, status, Query
from uuid import UUID

import api.schemas as fff_schema

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

@router.get("/transaction/{id}", response_model=fff_schema.Transaction)
def get_transaction(id: int):
	pass

@router.post("/transaction", response_model=fff_schema.TransactionOut, status_code=status.HTTP_201_CREATED)
def post_transaction(t_item: fff_schema.TransactionIn):
	return fff_schema.TransactionOut(id=1, **t_item.dict())

@router.put("/transaction/{id}", response_model=fff_schema.TransactionOut)
def put_transaction(id: int, t_item: fff_schema.TransactionIn):
	return fff_schema.TransactionOut(id=id, **t_item.dict())

@router.delete("/transaction/{id}", response_model=fff_schema.TransactionsMessage)
def delete_transaction(id: int):
	return fff_schema.TransactionsMessage(message="Deleted transaction", tids=[id])

@router.get("/transactions/{year}/{month}/{day}", response_model=list[fff_schema.TransactionOut])
def get_transactions_for_day(year: int, month: int, day: int):
	pass

@router.get("/transactions", response_model=list[fff_schema.TransactionOut])
def get_transactions_with_ids(tids: str):
	pass

@router.get("/transactions/series/{series}", response_model=list[fff_schema.TransactionOut])
def get_transactions_in_series(series: UUID):
	pass

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
