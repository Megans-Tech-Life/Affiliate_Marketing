from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from core.dependencies import get_db
from .models import Account
from .schemas import AccountResponse, AccountCreate

router = APIRouter(prefix="/accounts", tags=["Accounts"])

# Get all accounts
@router.get("/", response_model=List[AccountResponse])
def get_accounts(db: Session = Depends(get_db)):
    return db.query(Account).all()

# Get single account by ID
@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: UUID, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

# Create a new account
@router.post("/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    new_account = Account(
        company_name=account.name,
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

# Update an existing account
@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account_id: UUID, account_update: AccountCreate, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    account.company_name = account_update.name
    account.industry = account_update.industry
    account.website = account_update.website
    account.phone_code = account_update.phone_code
    account.phone_no = account_update.phone_no
    account.email = account_update.email
    account.address = account_update.address
    account.social_links = account_update.social_links
    account.legal_details = account_update.legal_details
    account.parent_account_id = account_update.parent_account_id

    db.commit()
    db.refresh(account)
    return account

# Delete an account
@router.delete("/{account_id}", response_model=dict)
def delete_account(account_id: UUID, db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(account)
    db.commit()
    return {"message": f"Account {account_id} deleted successfully"}

# Get contacts for an account
@router.get("/{account_id}/contacts")
def get_account_contacts(account_id: UUID, db: Session = Depends(get_db)):
    """Get all contacts (leads) for a specific account"""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    contacts = [
        {
            "id": contact.id,
            "title": contact.title,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
            "phone_code": contact.phone_code,
            "phone_no": contact.phone_no,
            "created_at": contact.created_at
        }
        for contact in account.contacts
    ]
    
    return {
        "account_id": account_id,
        "account_name": account.company_name,
        "contacts": contacts,
        "total_contacts": len(contacts)
    }