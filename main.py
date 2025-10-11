from fastapi import FastAPI
from core.database import Base, engine

from apps.accounts.routes import router as accounts_router
from apps.leads.routes import router as leads_router
# TODO: Add qualified, interested, and clients routers when implemented

from auth import router as auth_router 

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sales Funnel API", version="1.0.0")

# Register Routers 
app.include_router(accounts_router)
app.include_router(leads_router)
app.include_router(auth_router)
# TODO: Add qualified, interested, and clients routers when the modules are implemented:


@app.get("/")
def read_root():
    return {"message": "Sales Funnel API is running! (Accounts and Leads modules active)"}