from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import List, Tuple, Optional
from datetime import date
import calendar

import api.models as fff_model
import api.schemas as fff_schema
from api.cruds.other import get_user_ids_in_group

# Get Operations

#  d888b  d88888b d888888b 
# 88' Y8b 88'     `~~88~~' 
# 88      88ooooo    88    
# 88  ooo 88~~~~~    88    
# 88. ~8~ 88.        88    
#  Y888P  Y88888P    YP            

async def get_transaction(id: int, current_user_group: fff_schema.UserGroup, db: AsyncSession) -> Optional[fff_model.Transaction]:
	u_ids = await get_user_ids_in_group(current_user_group, db)

	clauses = [fff_model.Transaction.user_id.in_(u_ids), fff_model.Transaction.id == id]

	result: Result = await db.execute(
		select(fff_model.Transaction).filter(*clauses)
	)
	t: Optional[Tuple[fff_model.Transaction]] = result.fetchone()
	return t[0] if t is not None else None


async def get_transactions(ids: list[int], current_user_group: fff_schema.UserGroup, db: AsyncSession) -> List[fff_model.Transaction]:
	u_ids = await get_user_ids_in_group(current_user_group, db)

	clauses = [fff_model.Transaction.user_id.in_(u_ids), fff_model.Transaction.id.in_(ids)]

	result: Result = await db.execute(
		select(fff_model.Transaction).filter(*clauses)
	)
	transactions = list(map(lambda x: x[0], result.fetchall()))
	return transactions

async def get_transactions_in_series(series: str, current_user_group: fff_schema.UserGroup, db: AsyncSession) -> List[fff_model.Transaction]:
	u_ids = await get_user_ids_in_group(current_user_group, db)

	clauses = [fff_model.Transaction.user_id.in_(u_ids), fff_model.Transaction.series == series]

	result: Result = await db.execute(
		select(fff_model.Transaction).filter(*clauses)
	)
	transactions = list(map(lambda x: x[0], result.fetchall()))
	return transactions

async def get_transactions_for_date(year: int, month: int, day: int, c: fff_schema.TransactionTypeCategory, tt: int,
		current_user_group: fff_schema.UserGroup,
		db: AsyncSession) -> List[fff_model.Transaction]:
	u_ids = await get_user_ids_in_group(current_user_group, db)
	month_range = calendar.monthrange(year, month)
	q_date = date(year, month, min(day, month_range[1]))

	clauses = [fff_model.Transaction.user_id.in_(u_ids), fff_model.Transaction.transaction_date == q_date]
	if c != fff_schema.TransactionTypeCategory.all:
		clauses.append(fff_model.TransactionType.category == c)
	if tt != -1:
		clauses.append(fff_model.Transaction.transaction_type_id == tt)

	result: Result = await db.execute(
		select(fff_model.Transaction).join(fff_model.TransactionType).filter(*clauses)
	)
	transactions = list(map(lambda x: x[0], result.fetchall()))
	return transactions

async def get_transactions_for_month(year: int, month: int, c: fff_schema.TransactionTypeCategory, tt: int,
		current_user_group: fff_schema.UserGroup,
		db: AsyncSession) -> List[fff_model.Transaction]:
	u_ids = await get_user_ids_in_group(current_user_group, db)
	month_range = calendar.monthrange(year, month)
	first_of_month = date(year, month, 1)
	last_of_month = date(year, month, month_range[1])

	clauses = [fff_model.Transaction.user_id.in_(u_ids), 
				fff_model.Transaction.transaction_date >= first_of_month, 
				fff_model.Transaction.transaction_date <= last_of_month]
	if c != fff_schema.TransactionTypeCategory.all:
		clauses.append(fff_model.TransactionType.category == c)
	if tt != -1:
		clauses.append(fff_model.Transaction.transaction_type_id == tt)

	result: Result = await db.execute(
		select(fff_model.Transaction).join(fff_model.TransactionType).filter(*clauses)
	)
	transactions = list(map(lambda x: x[0], result.fetchall()))
	return transactions



# Single Transaction Edit Operations

# d88888b d8888b. d888888b d888888b 
# 88'     88  `8D   `88'   `~~88~~' 
# 88ooooo 88   88    88       88    
# 88~~~~~ 88   88    88       88    
# 88.     88  .8D   .88.      88    
# Y88888P Y8888D' Y888888P    YP    
                                  
                                  
async def create_transaction(t: fff_schema.TransactionIn, current_user: fff_schema.User, db: AsyncSession) -> fff_model.Transaction:
	transaction = fff_model.Transaction(**t.dict())
	transaction.user_id = current_user.id
	db.add(transaction)
	await db.commit()
	await db.refresh(transaction)
	return transaction

async def update_transaction(original: fff_model.Transaction, 
							updated_t: fff_schema.TransactionIn, 
							db: AsyncSession) -> fff_model.Transaction:
	original.amount = updated_t.amount
	original.description = updated_t.description
	original.series = updated_t.series
	original.transaction_date = updated_t.transaction_date
	original.transaction_type_id = updated_t.transaction_type_id
	db.add(original)
	await db.commit()
	await db.refresh(original)
	return original

async def delete_transaction(original: fff_model.Transaction, db: AsyncSession) -> None:
	await db.delete(original)
	await db.commit()

# Multiple Transaction Edit Operations

# .88b  d88. db    db db      d888888b d888888b        d88888b d8888b. d888888b d888888b 
# 88'YbdP`88 88    88 88      `~~88~~'   `88'          88'     88  `8D   `88'   `~~88~~' 
# 88  88  88 88    88 88         88       88           88ooooo 88   88    88       88    
# 88  88  88 88    88 88         88       88    C8888D 88~~~~~ 88   88    88       88    
# 88  88  88 88b  d88 88booo.    88      .88.          88.     88  .8D   .88.      88    
# YP  YP  YP ~Y8888P' Y88888P    YP    Y888888P        Y88888P Y8888D' Y888888P    YP    

async def create_transactions(t_list: list[fff_schema.TransactionIn], current_user: fff_schema.User, db: AsyncSession) -> List[fff_model.Transaction]:
	transactions = list(map(lambda t: fff_model.Transaction(**t.dict()), t_list))
	for transaction in transactions:
		transaction.user_id = current_user.id

	db.add_all(transactions)
	await db.commit()

	for transaction in transactions:
		await db.refresh (transaction)
	return transactions

async def update_transactions(originals: list[fff_model.Transaction],
							 updated: list[fff_schema.TransactionInWithID], 
							 db: AsyncSession) -> List[fff_model.Transaction]:
	for original, updated_t in zip(originals, updated):
		original.amount = updated_t.amount
		original.description = updated_t.description
		original.series = updated_t.series
		original.transaction_date = updated_t.transaction_date
		original.transaction_type_id = updated_t.transaction_type_id
		db.add(original)
	await db.commit()
	for original in originals:
		await db.refresh(original)
	return originals


async def delete_transactions(originals: list[fff_model.Transaction], db: AsyncSession) -> list[int]:
	t_ids = []
	for original in originals:
		t_ids.append(original.id)
		await db.delete(original)
	await db.commit()
	return t_ids