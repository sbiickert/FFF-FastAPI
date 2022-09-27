from pydantic import BaseModel, Field, EmailStr, Json
from enum import Enum
from uuid import UUID
import datetime

# USER

class UserBase(BaseModel):
	email: EmailStr
	roles: Json
	user_group_id: int
	short_name: str
	full_name: str

class UserOut(UserBase):
	id: int

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


# TRANSACTION 

class TransactionBase(BaseModel):
	amount: float
	description: str
	transaction_date: datetime.date
	series: UUID

class TransactionIn(TransactionBase):
	user_id: int
	transaction_type_id: int

class Transaction(TransactionBase):
	id: int
	transaction_type: TransactionType
	user: UserOut

class TransactionOut(TransactionIn):
	id: int

class TransactionsMessage(BaseModel):
	message: str
	tids: list[int]