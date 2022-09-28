from unittest import result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import List, Tuple, Optional
import datetime

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

async def get_transactions_for_date(year: int, month: int, day: int | None, c: str, tt: int,
		db: AsyncSession) -> List[fff_model.Transaction]:
	result: Result = await db.execute(
		select(fff_model.Transaction).filter(fff_model.Transaction.transaction_date.l)
	)

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
