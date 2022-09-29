from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from typing import Optional, Tuple

import api.models as fff_model
import api.schemas as fff_schema

async def get_transaction_type(id: int, db: AsyncSession) -> Optional[fff_model.TransactionType]:
	result: Result = await db.execute(
		select(fff_model.TransactionType).filter(fff_model.TransactionType.id == id)
	)
	t: Optional[Tuple[fff_model.TransactionType]] = result.fetchone()
	return t[0] if t is not None else None

async def get_transaction_types(category: fff_schema.TransactionTypeCategory, db: AsyncSession) -> list[fff_model.TransactionType]:
	result: Result = await db.execute(
		select(fff_model.TransactionType).filter(fff_model.TransactionType.category == category)
	)
	tt_list = list(map(lambda x: x[0], result.fetchall()))
	return tt_list
