Transactional Ledger Service
Author

Name: Jayalakshmi MB
Designation: Python Developer / Full Stack

Overview

This project implements a simplified transactional ledger service. It supports account creation, balance management, transaction history, deposits/withdrawals, and internal transfers. The focus is on financial accuracy, data integrity, and proper handling of concurrent transactions.

The APIs are built using FastAPI with PostgreSQL as the backend database.

Features / APIs
No API Endpoint Method Description
1 /accounts GET List all accounts
2 /accounts POST Create a new account
3 /accounts/{account_id} GET Get full account info
4 /accounts/{account_id}/balance GET Get only account balance
5 /transactions POST Deposit or withdraw funds
6 /transactions/{account_id} GET Transaction history for an account
7 /transactions/id/{transaction_id} GET Get single transaction (optional)
8 /transfers POST Transfer funds between accounts
9 /test-route GET Health check endpoint
Database Choice & Schema

Database: PostgreSQL

Reason for choice:

Supports ACID transactions, which is essential for financial data integrity.

Strong support for concurrency control to prevent double-spending.

Easy integration with SQLAlchemy ORM for Python.

Schema Overview:

Accounts Table

id (Primary Key)

name (Unique)

currency

balance (Decimal)

created_at / updated_at

Transactions Table

id (Primary Key)

account_id (Foreign Key → Accounts.id)

type (credit/debit)

amount (Decimal)

description (Optional)

created_at

This design ensures each transaction is linked to an account and balances are updated atomically.

Concurrency Strategy

To prevent double-spending:

Atomic database operations are used to ensure updates to balances and transactions are committed together.

SQLAlchemy’s session is used to manage transactions with commit and refresh.

All critical operations (debit/credit/transfer) validate the balance before committing, avoiding overdrafts.

Trade-offs & Scaling Considerations

If this system needed to handle 1 million transactions per second:

Introduce sharding or partitioning of accounts.

Use distributed transaction queues or event-driven architecture instead of synchronous DB writes.

Employ optimistic locking and caching layers to reduce database contention.

Consider a NoSQL solution like MongoDB for high throughput, but with extra caution for consistency.

Installation

Clone the repository:

git clone <your-repo-link>
cd txn-ledger

Create virtual environment and install dependencies:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Run PostgreSQL and set connection in .env file.

Run migrations (if using Alembic) or create tables manually.

Start the FastAPI server:

uvicorn app.main:app --reload

Open Postman or browser:

Swagger docs: http://127.0.0.1:8000/docs

Postman / API Testing

A Postman collection is provided with all endpoints.

You can test create account, deposit, withdraw, transfer, and history APIs with sample JSON payloads.

Sample JSON for creating an account:

{
"name": "Riya",
"currency": "INR",
"balance": 500
}

Sample JSON for transaction (deposit/withdraw):

{
"account_id": 1,
"type": "credit",
"amount": 500,
"description": "Salary"
}

Sample JSON for transfer:

{
"from_id": 1,
"to_id": 2,
"amount": 200
}

Notes

description field is optional. If not provided, it defaults to an empty string "".

All monetary operations are atomic, ensuring consistent balances.

Error handling returns proper HTTP status codes (404, 400).
