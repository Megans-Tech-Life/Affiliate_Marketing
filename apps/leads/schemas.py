from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

class LeadCreate(BaseModel):
    title: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone_code: Optional[str] = None
    phone_no: Optional[str] = None
    entry_point: Optional[str] = "INDV"
    platform: Optional[str] = None
    account_ids: List[uuid.UUID] = [] # List of associated account IDs

class LeadResponse(BaseModel):
    id: uuid.UUID
    title: str
    first_name: str
    last_name: str
    email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Contact-focused schemas (since leads serve as contacts)
class ContactBase(BaseModel):
    """Base schema for contact information"""
    title: str
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone_code: Optional[str] = None
    phone_no: Optional[str] = None

class ContactResponse(BaseModel):
    """Response schema for contact data"""
    id: uuid.UUID
    title: str
    first_name: str
    last_name: str
    email: Optional[str]
    phone_code: Optional[str]
    phone_no: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True