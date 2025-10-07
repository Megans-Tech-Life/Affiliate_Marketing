from fastapi import FastAPI
from routes.auth import router as auth_router
from routes.leads import router as leads_router
from routes.accounts import router as accounts_router

from database import engine
import models

# Create database tables
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Affiliate Marketing Accounts API", version="1.0.0")

# Include Routers
app.include_router(auth_router)
app.include_router(leads_router)
app.include_router(accounts_router)

@app.get("/")
def read_root():
    return {"message": "Affiliate Marketing Accounts API is running!"}