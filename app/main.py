from fastapi import FastAPI
from .db import Base, engine
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Transactional Ledger Service",
    version="1.0"
)

# Register routes
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Ledger API Running Successfully!"}
