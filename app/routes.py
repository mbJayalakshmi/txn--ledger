from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from . import crud, schemas
from typing import List

router = APIRouter()

@router.get("/test-route")
def test_route():
    return {"status": "ok"}

@router.get("/accounts", response_model=List[schemas.AccountResponse])
def list_accounts(db: Session = Depends(get_db)):
    return crud.get_all_accounts(db)

@router.get("/accounts/{account_id}", response_model=schemas.AccountResponse)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = crud.get_account(db, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.get("/accounts/{account_id}/balance")
def get_account_balance(account_id: int, db: Session = Depends(get_db)):
    account = crud.get_account(db, account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account.id, "balance": float(account.balance)}

@router.post("/accounts", response_model=schemas.AccountResponse)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    return crud.create_account(db, account)


@router.post("/transactions", response_model=schemas.TransactionResponse)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    result = crud.create_transaction(db, transaction)
    if result is None:
        raise HTTPException(status_code=400, detail="Transaction failed")
    return result

@router.get("/transactions/{account_id}", response_model=schemas.TransactionHistoryResponse)
def transaction_history(account_id: int, db: Session = Depends(get_db)):
    history = crud.get_transaction_history(db, account_id)
    if history is None:
        raise HTTPException(status_code=404, detail="No transactions found for this account")
    return history



@router.post("/transfers")
def transfer(data: schemas.TransferCreate, db: Session = Depends(get_db)):
    success = crud.transfer_funds(db, data.from_id, data.to_id, data.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Transfer failed")
    return {"message": "Transfer successful"}


@router.get("/transactions/id/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    tx = crud.get_transaction_by_id(db, transaction_id)
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx
