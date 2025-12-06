# app/crud.py
from sqlalchemy.orm import Session
from .models import Account, Transaction
from .schemas import AccountCreate, TransactionCreate, TransactionHistoryResponse, AccountResponse
from datetime import datetime
from decimal import Decimal

def create_account(db: Session, account: AccountCreate):
    # Prevent duplicate names (UNIQUE constraint protection)
    existing = db.query(Account).filter(Account.name == account.name).first()
    if existing:
        return None  # caller should return 400

    new_acc = Account(
        name=account.name,
        currency=account.currency,
        balance=Decimal(str(account.balance))
    )
    db.add(new_acc)
    db.commit()
    db.refresh(new_acc)
    return new_acc

def get_all_accounts(db: Session):
    return db.query(Account).all()

def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()

def create_transaction(db: Session, tx: TransactionCreate):
    account = db.query(Account).filter(Account.id == tx.account_id).first()
    if not account:
        return None

    amount = Decimal(str(tx.amount))

    if tx.type == "credit":
        account.balance += amount

    elif tx.type == "debit":
        if account.balance < amount:
            return None
        account.balance -= amount

    else:
        return None

    new_tx = Transaction(
        account_id=tx.account_id,
        type=tx.type,
        amount=amount,
        description=tx.description or "",  # ensure description is not null
        created_at=datetime.utcnow()
    )

    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx

def get_transaction_history(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        return None

    tx_list = (
        db.query(Transaction)
        .filter(Transaction.account_id == account_id)
        .order_by(Transaction.created_at.desc())
        .all()
    )

    account_data = AccountResponse.from_orm(account)

    return TransactionHistoryResponse(
        account=account_data,
        transactions=tx_list
    )

def transfer_funds(db: Session, from_id: int, to_id: int, amount: float):
    amount = Decimal(str(amount))

    from_acc = db.query(Account).filter(Account.id == from_id).first()
    to_acc = db.query(Account).filter(Account.id == to_id).first()

    if not from_acc or not to_acc:
        return False

    if from_acc.balance < amount:
        return False

    from_acc.balance -= amount
    to_acc.balance += amount

    tx_out = Transaction(
        account_id=from_id,
        type="debit",
        amount=amount,
        description="Transfer Out",
        created_at=datetime.utcnow(),
    )
    tx_in = Transaction(
        account_id=to_id,
        type="credit",
        amount=amount,
        description="Transfer In",
        created_at=datetime.utcnow(),
    )

    db.add_all([tx_out, tx_in])
    db.commit()
    return True

def get_transaction_by_id(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()
