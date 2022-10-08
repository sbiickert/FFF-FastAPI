from unicodedata import category
from unittest import result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, text
from sqlalchemy.engine import Result
from typing import Optional, Tuple
import calendar

import api.models as fff_model
import api.schemas as fff_schema

# d888888b d8888b.  .d8b.  d8b   db .d8888.  .d8b.   .o88b. d888888b d888888b  .d88b.  d8b   db 
# `~~88~~' 88  `8D d8' `8b 888o  88 88'  YP d8' `8b d8P  Y8 `~~88~~'   `88'   .8P  Y8. 888o  88 
#    88    88oobY' 88ooo88 88V8o 88 `8bo.   88ooo88 8P         88       88    88    88 88V8o 88 
#    88    88`8b   88~~~88 88 V8o88   `Y8b. 88~~~88 8b         88       88    88    88 88 V8o88 
#    88    88 `88. 88   88 88  V888 db   8D 88   88 Y8b  d8    88      .88.   `8b  d8' 88  V888 
#    YP    88   YD YP   YP VP   V8P `8888Y' YP   YP  `Y88P'    YP    Y888888P  `Y88P'  VP   V8P 
                                                                                              
# d888888b db    db d8888b. d88888b .d8888.                                                     
# `~~88~~' `8b  d8' 88  `8D 88'     88'  YP                                                     
#    88     `8bd8'  88oodD' 88ooooo `8bo.                                                       
#    88       88    88~~~   88~~~~~   `Y8b.                                                     
#    88       88    88      88.     db   8D                                                     
#    YP       YP    88      Y88888P `8888Y'                                                     
                                                                                              
                                                                                              
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

# db    db .d8888. d88888b d8888b. 
# 88    88 88'  YP 88'     88  `8D 
# 88    88 `8bo.   88ooooo 88oobY' 
# 88    88   `Y8b. 88~~~~~ 88`8b   
# 88b  d88 db   8D 88.     88 `88. 
# ~Y8888P' `8888Y' Y88888P 88   YD 
                                 
async def get_user(user_email: str, db: AsyncSession) -> fff_model.User | None:
	result: Result = await db.execute(
		select(fff_model.User).filter(fff_model.User.email == user_email)
	)
	t: Optional[Tuple[fff_model.User]] = result.fetchone()
	return t[0] if t is not None else None

async def get_user_group(user_group_id: int, db: AsyncSession) -> fff_model.UserGroup | None:
	result: Result = await db.execute(
		select(fff_model.UserGroup).filter(fff_model.UserGroup.id == user_group_id)
	)
	t: Optional[Tuple[fff_model.UserGroup]] = result.fetchone()
	return t[0] if t is not None else None

async def get_users_in_group(user_group: fff_schema.UserGroup, db: AsyncSession) -> list[fff_model.User]:
	result: Result = await db.execute(
		select(fff_model.User).filter(fff_model.User.user_group_id == user_group.id)
	)
	u_list = list(map(lambda x: x[0], result.fetchall()))
	return u_list

async def get_user_ids_in_group(user_group: fff_schema.UserGroup, db: AsyncSession) -> list[int]:
	users = await get_users_in_group(user_group, db)
	return list(map(lambda u: u.id, users))


# .d8888. d88888b  .d8b.  d8888b.  .o88b. db   db 
# 88'  YP 88'     d8' `8b 88  `8D d8P  Y8 88   88 
# `8bo.   88ooooo 88ooo88 88oobY' 8P      88ooo88 
#   `Y8b. 88~~~~~ 88~~~88 88`8b   8b      88~~~88 
# db   8D 88.     88   88 88 `88. Y8b  d8 88   88 
# `8888Y' Y88888P YP   YP 88   YD  `Y88P' YP   YP 

async def search_transactions(query: str, current_user_group: fff_schema.UserGroup, db: AsyncSession) -> list[fff_model.Transaction]:
	u_ids = await get_user_ids_in_group(current_user_group, db)

	clauses = [fff_model.Transaction.description.like(query), fff_model.Transaction.user_id.in_(u_ids)]
	
	result: Result = await db.execute(
		select(fff_model.Transaction).filter(*clauses)
	)
	t_list = list(map(lambda x: x[0], result.fetchall()))
	return t_list

# .d8888. db    db .88b  d88. .88b  d88.  .d8b.  d8888b. db    db 
# 88'  YP 88    88 88'YbdP`88 88'YbdP`88 d8' `8b 88  `8D `8b  d8' 
# `8bo.   88    88 88  88  88 88  88  88 88ooo88 88oobY'  `8bd8'  
#   `Y8b. 88    88 88  88  88 88  88  88 88~~~88 88`8b      88    
# db   8D 88b  d88 88  88  88 88  88  88 88   88 88 `88.    88    
# `8888Y' ~Y8888P' YP  YP  YP YP  YP  YP YP   YP 88   YD    YP    

async def get_summary_for_month(year: int, month: int,
		current_user_group: fff_schema.UserGroup,
		db: AsyncSession) -> list[fff_schema.Summary]:

	u_ids = await get_user_ids_in_group(current_user_group, db)
	user_group_clause = build_user_group_clause(u_ids)

	sql = 't.transaction_type_id, tt.name, tt.category category, SUM(t.amount) amount'
	sql += ' FROM TRANSACTION t, transaction_type tt'
	sql += f' WHERE t.transaction_type_id = tt.id AND YEAR(t.transaction_date) = {year}'
	if month > 0:
		sql += f'  AND MONTH(t.transaction_date) = {month}'
	sql += f' AND {user_group_clause}'
	sql += ' GROUP BY t.transaction_type_id, category'

	text_sql = text(sql)
	result: Result = await db.execute(
		select(text_sql)
	)

	summary = []
	for row in result.fetchall():
		s = fff_schema.Summary(tt=row[0], tt_name=row[1], category=row[2], amount=row[3], percent=0)
		summary.append(s)

	# Calculate percentages
	sum_expense = sum(list(map(lambda s: s.amount, filter(lambda s: (s.category == 'EXPENSE'), summary))))
	sum_income = sum(list(map(lambda s: s.amount, filter(lambda s: (s.category == 'INCOME'), summary))))

	for s in summary:
		if s.category == 'EXPENSE' and sum_expense > 0:
			s.percent = s.amount / sum_expense
		if s.category == 'INCOME' and sum_income > 0:
			s.percent = s.amount / sum_income

	return summary


# d8888b.  .d8b.  db       .d8b.  d8b   db  .o88b. d88888b 
# 88  `8D d8' `8b 88      d8' `8b 888o  88 d8P  Y8 88'     
# 88oooY' 88ooo88 88      88ooo88 88V8o 88 8P      88ooooo 
# 88~~~b. 88~~~88 88      88~~~88 88 V8o88 8b      88~~~~~ 
# 88   8D 88   88 88booo. 88   88 88  V888 Y8b  d8 88.     
# Y8888P' YP   YP Y88888P YP   YP VP   V8P  `Y88P' Y88888P 

async def get_balance_for_date(year: int, month: int, day: int,
		current_user_group: fff_schema.UserGroup,
		db: AsyncSession) -> fff_schema.BalanceReport:

	u_ids = await get_user_ids_in_group(current_user_group, db)
	user_group_clause = build_user_group_clause(u_ids)

	report = await get_balance_for_month(year, month, current_user_group, db, include_day_balances=False)
	report.day = day

	text_sql = text(build_balance_for_day_query(year, month, day, user_group_clause))
	result: Result = await db.execute(
		select(text_sql)
	)

	# There 0 to 2 rows. Once for EXPENSE and the other for INCOME
	b = fff_schema.Balance()
	b.index = day

	for row in result.fetchall():
		if row[1] == 'EXPENSE':
			b.expense = row[2]
		else:
			b.income = row[2]
		b.calc_diff()

	report.day_balances.append(b)
	
	return report

async def get_balance_for_month(year: int, month: int,
		current_user_group: fff_schema.UserGroup,
		db: AsyncSession,
		include_day_balances: bool = True) -> fff_schema.BalanceReport:

	u_ids = await get_user_ids_in_group(current_user_group, db)
	user_group_clause = build_user_group_clause(u_ids)

	report = await get_balance_for_year(year, current_user_group, db)
	report.month = month

	text_sql = text(build_balance_for_month_query(year, month, user_group_clause))
	result: Result = await db.execute(
		select(text_sql)
	)

	# There are two rows. Once for EXPENSE and the other for INCOME
	# (8, 'EXPENSE', Decimal('14567.56'))
	# (8, 'INCOME', Decimal('15225.85'))
	b = fff_schema.Balance()
	b.index = month
	for row in result.fetchall():
		if row[1] == 'EXPENSE':
			b.expense = row[2]
		else:
			b.income = row[2]
	b.calc_diff()

	for m in range(1, 13):
		if m == month:
			report.month_balances.append(b)
		else:
			report.month_balances.append(fff_schema.Balance(index=m))


	# Day balances. Default is to query them.
	if include_day_balances:
		day_bal_lookup = {}
		month_range = calendar.monthrange(year, month)

		for d in range(1, month_range[1]+1):
			b = fff_schema.Balance(index=d)
			report.day_balances.append(b)
			day_bal_lookup[d] = b

		text_sql = text(build_balance_for_day_query(year, month, -1, user_group_clause))
		result: Result = await db.execute(
			select(text_sql)
		)
		# There 0 to 2 rows for each day. Once for EXPENSE and the other for INCOME
		for row in result.fetchall():
			if row[1] == 'EXPENSE':
				day_bal_lookup[row[0]].expense = row[2]
			else:
				day_bal_lookup[row[0]].income = row[2]
			day_bal_lookup[row[0]].calc_diff()

	return report

async def get_balance_for_year(year: int,
		current_user_group: fff_schema.UserGroup,
		db: AsyncSession) -> fff_schema.BalanceReport:

	u_ids = await get_user_ids_in_group(current_user_group, db)
	user_group_clause = build_user_group_clause(u_ids)

	text_sql = text(build_balance_for_year_query(year, user_group_clause))
	result: Result = await db.execute(
		select(text_sql)
	)

	report = fff_schema.BalanceReport(year=-1, month=-1, day=-1, 
										year_balance=fff_schema.Balance(), 
										month_balances=[], 
										day_balances=[])
	report.year = year

	# There are two rows. Once for EXPENSE and the other for INCOME
	# (2022, 'EXPENSE', Decimal('111297.76'))
	# (2022, 'INCOME', Decimal('140965.28'))
	for row in result.fetchall():
		if row[1] == 'EXPENSE':
			report.year_balance.expense = row[2]
		else:
			report.year_balance.income = row[2]
	
	report.year_balance.calc_diff()

	return report


# .d8888.  .d88b.  db      
# 88'  YP .8P  Y8. 88      
# `8bo.   88    88 88      
#   `Y8b. 88    88 88      
# db   8D `8P  d8' 88booo. 
# `8888Y'  `Y88'Y8 Y88888P 


def build_user_group_clause(u_ids: list[int]) -> str:
	u_ids_str = [str(id) for id in u_ids]
	return f"user_id in ({','.join(u_ids_str)})"

def build_balance_for_year_query(year: int, user_group_clause: str) -> str:
	sql = 'YEAR(transaction_date) YEAR, tt.category category, SUM(t.amount) amount'
	sql += ' FROM transaction t, transaction_type tt'
	sql += ' WHERE t.transaction_type_id = tt.id'
	sql += f' AND YEAR(transaction_date) = {year} AND {user_group_clause}'
	sql += ' GROUP BY YEAR, category'
	return sql

def build_balance_for_month_query(year: int, month: int, user_group_clause: str) -> str:
	sql = 'MONTH(t.transaction_date) month, tt.category category, SUM(t.amount) amount'
	sql += ' FROM transaction t, transaction_type tt'
	sql += f' WHERE t.transaction_type_id = tt.id and YEAR(transaction_date) = {year}'
	sql += f' AND MONTH(t.transaction_date) = {month} AND {user_group_clause}'
	sql += ' GROUP BY month, category'
	return sql

def build_balance_for_day_query(year: int, month: int, day: int, user_group_clause: str) -> str:
	sql = 'DAY(t.transaction_date) day, tt.category category, SUM(t.amount) amount'
	sql += ' FROM transaction t, transaction_type tt'
	sql += f' WHERE t.transaction_type_id = tt.id and YEAR(transaction_date) = {year}'
	sql += f' AND MONTH(t.transaction_date) = {month} AND {user_group_clause}'
	if (day > 0):
		sql += f' AND DAY(t.transaction_date) = {day}'
	sql += ' GROUP BY day, category'
	return sql