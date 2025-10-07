from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from database import SessionLocal
import models, schemas

router = APIRouter(prefix="/leads", tags=["Leads"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all leads
@router.get("/", response_model=List[schemas.LeadResponse])
def get_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).all()

# Get single lead by ID
@router.get("/{lead_id}", response_model=schemas.LeadResponse)
def get_lead(lead_id: UUID, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

# Create a new lead
@router.post("/", response_model=schemas.LeadResponse)
def create_lead(lead: schemas.LeadCreate, db: Session = Depends(get_db)):
    new_lead = models.Lead(
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
        accounts = db.query(models.Account).filter(models.Account.id.in_(lead.account_ids)).all()
        if len(accounts) != len(lead.account_ids):
            raise HTTPException(status_code=404, detail="One or more accounts not found")
        new_lead.accounts = accounts

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    return new_lead

# Update an existing lead
@router.put("/{lead_id}", response_model=schemas.LeadResponse)
def update_lead(lead_id: UUID, lead_update: schemas.LeadCreate, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
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
        accounts = db.query(models.Account).filter(models.Account.id.in_(lead_update.account_ids)).all()
        if len(accounts) != len(lead_update.account_ids):
            raise HTTPException(status_code=404, detail="One or more accounts not found")
        lead.accounts = accounts

    db.commit()
    db.refresh(lead)
    return lead

# Delete a lead
@router.delete("/{lead_id}", response_model=dict)
def delete_lead(lead_id: UUID, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db.delete(lead)
    db.commit()
    return {"message": f"Lead {lead_id} deleted successfully"}