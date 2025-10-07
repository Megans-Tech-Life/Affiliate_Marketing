from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime


# Schemas for Account
class AccountBase(BaseModel):
    id: uuid.UUID
    name: str

    class Config:
        from_attributes = True

class AccountCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    phone_code: Optional[str] = None
    phone_no: Optional[str] = None
    email: Optional[str] = None
    address: Optional[dict] = None
    social_links: Optional[dict] = None
    legal_details: Optional[dict] = None
    parent_account_id: Optional[uuid.UUID] = None

class AccountResponse(AccountBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Schemas for Lead
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
    accounts: List[AccountBase] = []
    created_at: datetime

    class Config:
        from_attributes = True