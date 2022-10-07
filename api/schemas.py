from pydantic import BaseModel, Field, EmailStr
from enum import Enum
from uuid import UUID
import datetime

# USER

class UserBase(BaseModel):
	email: EmailStr
	roles: str
	user_group_id: int
	short_name: str
	full_name: str

class UserOut(UserBase):
	id: int
	class Config:
		orm_mode = True

class User(UserBase):
	id: int
	password: str
	class Config:
		orm_mode = True


# USER GROUP

class UserGroup(BaseModel):
	id: int
	name: str
	users: list[User]


# TOKEN

class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	username: str | None = None

# TRANSACTION TYPE

class TransactionTypeCategory(str, Enum):
	income = "INCOME"
	expense = "EXPENSE"
	all = "ALL"

class TransactionType(BaseModel):
	id: int
	name: str = Field("", title="The transaction type name", max_length=255)
	is_active: bool = Field(True, description="Is this transaction type valid for new transactions")
	category: TransactionTypeCategory = Field(TransactionTypeCategory.expense)
	symbol: str
	class Config:
		orm_mode = True


# TRANSACTION 

class TransactionBase(BaseModel):
	amount: float
	description: str | None
	transaction_date: datetime.date
	series: UUID | None

class TransactionIn(TransactionBase):
	user_id: int
	transaction_type_id: int

class TransactionInWithID(TransactionIn):
	id: int
	
class Transaction(TransactionBase):
	id: int
	transaction_type: TransactionType
	user: UserOut

class TransactionOut(TransactionIn):
	id: int
	class Config:
		orm_mode = True

class TransactionsMessage(BaseModel):
	message: str
	tids: list[int]


# BALANCE

class Balance(BaseModel):
	index: int
	income: float
	expense: float
	diff: float

class BalanceReport(BaseModel):
	year: int
	month: int
	day: int
	year_balance: Balance
	month_balances: list[Balance]
	day_balances: list[Balance]

# SUMMARY

class Summary(BaseModel):
	tt: int
	tt_name: str
	amount: float
	percent: float
	category: TransactionTypeCategory