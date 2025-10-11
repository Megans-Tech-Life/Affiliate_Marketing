from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

class AccountBase(BaseModel):
    id: uuid.UUID
    name: str = Field(alias="company_name")

    class Config:
        from_attributes = True
        populate_by_name = True

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
        populate_by_name = True