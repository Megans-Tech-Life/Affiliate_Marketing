from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from core.dependencies import get_db
from .models import Lead
from .schemas import LeadResponse, LeadCreate
from apps.accounts.models import Account

router = APIRouter(prefix="/leads", tags=["Leads"])

# Get all leads
@router.get("/", response_model=List[LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return db.query(Lead).all()

# Get single lead by ID
@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: UUID, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

# Create a new lead
@router.post("/", response_model=LeadResponse)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    new_lead = Lead(
        title=lead.title,
        first_name=lead.first_name,
        last_name=lead.last_name,
        email=lead.email,
        phone_code=lead.phone_code,
        phone_no=lead.phone_no,
        entry_point=lead.entry_point,
        platform=lead.platform
    )

    if lead.account_ids:
        accounts = db.query(Account).filter(Account.id.in_(lead.account_ids)).all()
        if len(accounts) != len(lead.account_ids):
            raise HTTPException(status_code=404, detail="One or more accounts not found")
        new_lead.accounts = accounts

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

# Update an existing lead
@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: UUID, lead_update: LeadCreate, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.title = lead_update.title
    lead.first_name = lead_update.first_name
    lead.last_name = lead_update.last_name
    lead.email = lead_update.email
    lead.phone_code = lead_update.phone_code
    lead.phone_no = lead_update.phone_no
    lead.entry_point = lead_update.entry_point
    lead.platform = lead_update.platform

    if lead_update.account_ids:
        accounts = db.query(Account).filter(Account.id.in_(lead_update.account_ids)).all()
        if len(accounts) != len(lead_update.account_ids):
            raise HTTPException(status_code=404, detail="One or more accounts not found")
        lead.accounts = accounts

    db.commit()
    db.refresh(lead)
    return lead

# Delete a lead
@router.delete("/{lead_id}", response_model=dict)
def delete_lead(lead_id: UUID, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db.delete(lead)
    db.commit()
    return {"message": f"Lead {lead_id} deleted successfully"}

# Contact-specific endpoints (since leads serve as contacts)

# Get all contacts for a specific account
@router.get("/contacts/account/{account_id}", response_model=List[LeadResponse])
def get_account_contacts(account_id: UUID, db: Session = Depends(get_db)):
    """Get all contacts (leads) associated with a specific account"""
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account.contacts

# Add a contact (lead) to an account
@router.post("/contacts/account/{account_id}/lead/{lead_id}", response_model=dict)
def add_contact_to_account(account_id: UUID, lead_id: UUID, db: Session = Depends(get_db)):
    """Associate a lead as a contact with an account"""
    account = db.query(Account).filter(Account.id == account_id).first()
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if lead not in account.contacts:
        account.contacts.append(lead)
        db.commit()
        return {"message": f"Lead {lead_id} added as contact to account {account_id}"}
    else:
        return {"message": f"Lead {lead_id} is already a contact for account {account_id}"}

# Remove a contact (lead) from an account
@router.delete("/contacts/account/{account_id}/lead/{lead_id}", response_model=dict)
def remove_contact_from_account(account_id: UUID, lead_id: UUID, db: Session = Depends(get_db)):
    """Remove association between a lead and an account"""
    account = db.query(Account).filter(Account.id == account_id).first()
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    if lead in account.contacts:
        account.contacts.remove(lead)
        db.commit()
        return {"message": f"Lead {lead_id} removed as contact from account {account_id}"}
    else:
        return {"message": f"Lead {lead_id} is not a contact for account {account_id}"}