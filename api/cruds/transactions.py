from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import List, Tuple, Optional

import api.models as fff_model
import api.schemas as fff_schema

async def create_transaction(db: AsyncSession, t: fff_schema.TransactionIn) -> fff_model.Transaction:
	transaction = fff_model.Transaction(**t.dict())
	db.add(transaction)
	await db.commit()
	await db.refresh(transaction)
	return transaction

async def get_transaction_with_id(db: AsyncSession, id: int) -> Optional[fff_model.Transaction]:
	result: Result = await db.execute(
		select(fff_model.Transaction).filter(fff_model.Transaction.id == id)
	)
	t: Optional[Tuple[fff_model.Transaction]] = result.fetchone()
	return t[0] if t is not None else None