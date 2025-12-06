from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .db import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, nullable=False)
    currency = Column(String(3), nullable=False)
    balance = Column(Numeric(20,2), default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    transactions = relationship("Transaction", back_populates="account")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    type = Column(String(10), nullable=False)  # 'credit' or 'debit'
    amount = Column(Numeric(20,2), nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    idempotency_key = Column(String, unique=True, nullable=True)
    account = relationship("Account", back_populates="transactions")



