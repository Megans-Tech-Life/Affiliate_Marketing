from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
from typing import Optional

router = APIRouter(prefix="/accounts", tags=["Accounts"])

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AccountResponse)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    new_account = models.Account(
        name=account.name,
        industry=account.industry,
        website=account.website,
        phone_code=account.phone_code,
        phone_no=account.phone_no,
        email=account.email,
        address=account.address,
        social_links=account.social_links,
        legal_details=account.legal_details,
        parent_account_id=account.parent_account_id
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account

@router.get("/", response_model=list[schemas.AccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    return db.query(models.Account).all()