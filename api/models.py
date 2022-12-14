from sqlalchemy import Column, Integer, String, Numeric, Date, JSON, ForeignKey
from sqlalchemy.orm import relationship

from api.db import Base

class TransactionType(Base):
	__tablename__ = "transaction_type"

	id = Column(Integer, primary_key=True)
	name = Column(String(255))
	is_active = Column(Integer, default=True)
	category = Column(String(255))
	symbol = Column(String(10, collation="utf8mb4_bin"))

class Transaction(Base):
	__tablename__ = "transaction"

	id = Column(Integer, primary_key=True)
	transaction_type_id = Column(Integer, ForeignKey("transaction_type.id"), nullable=False)
	user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
	amount = Column(Numeric(10,2), nullable=False)
	description = Column(String(255), nullable=True)
	transaction_date = Column(Date, nullable=False)
	series = Column(String(36), nullable=True)

class User(Base):
	__tablename__ = "user"

	id = Column(Integer, primary_key=True)
	user_group_id = Column(Integer, ForeignKey("user_group.id"))
	email = Column(String(180))
	roles = Column(String(255))
	password = Column(String(255))
	short_name = Column(String(255))
	full_name = Column(String(255))


class UserGroup(Base):
	__tablename__ = "user_group"

	id = Column(Integer, primary_key=True)
	name = Column(String(255))