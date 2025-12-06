from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class AccountCreate(BaseModel):
    name: str
    currency: str
    balance: float = 0.0   # default 0

class AccountResponse(BaseModel):
    id: int
    name: str
    currency: str
    balance: float
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TransactionType(str, Enum):
    credit = "credit"
    debit = "debit"

class TransactionCreate(BaseModel):
    account_id: int
    type: TransactionType
    amount: float
    description: Optional[str] = None
    idempotency_key: Optional[str] = None

class TransactionResponse(BaseModel):
    id: int
    account_id: int
    type: TransactionType
    amount: float
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True

class TransactionHistoryResponse(BaseModel):
    account: AccountResponse
    transactions: List[TransactionResponse]


class TransferCreate(BaseModel):
    from_id: int
    to_id: int
    amount: float
