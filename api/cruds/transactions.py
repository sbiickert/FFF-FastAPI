from unittest import result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import List, Tuple, Optional
from datetime import date
import calendar

import api.models as fff_model
import api.schemas as fff_schema

# Get Operations

async def get_transaction(id: int, db: AsyncSession) -> Optional[fff_model.Transaction]:
	result: Result = await db.execute(
		select(fff_model.Transaction).filter(fff_model.Transaction.id == id)
	)
	t: Optional[Tuple[fff_model.Transaction]] = result.fetchone()
	return t[0] if t is not None else None

async def get_transactions(ids: list[int], db: AsyncSession) -> List[fff_model.Transaction]:
	result: Result = await db.execute(
		select(fff_model.Transaction).filter(fff_model.Transaction.id.in_(ids))
	)
	transactions = list(map(lambda x: x[0], result.fetchall()))
	return transactions

async def get_transactions_in_series(series: str, db: AsyncSession) -> List[fff_model.Transaction]:
	result: Result = await db.execute(
		select(fff_model.Transaction).filter(fff_model.Transaction.series == series)
	)
	transactions = list(map(lambda x: x[0], result.fetchall()))
	return transactions

async def get_transactions_for_date(year: int, month: int, day: int, c: fff_schema.TransactionTypeCategory, tt: int,
		db: AsyncSession) -> List[fff_model.Transaction]:
	month_range = calendar.monthrange(year, month)
	q_date = date(year, month, min(day, month_range[1]))
	clauses = [fff_model.Transaction.transaction_date == q_date]
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
		db: AsyncSession) -> List[fff_model.Transaction]:
	month_range = calendar.monthrange(year, month)
	first_of_month = date(year, month, 1)
	last_of_month = date(year, month, month_range[1])
	clauses = [fff_model.Transaction.transaction_date >= first_of_month, fff_model.Transaction.transaction_date <= last_of_month]
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

async def create_transaction(t: fff_schema.TransactionIn, db: AsyncSession) -> fff_model.Transaction:
	transaction = fff_model.Transaction(**t.dict())
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
