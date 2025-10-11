import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from core.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = Column(String(255), nullable=False)
    industry = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    phone_code = Column(String(50), nullable=True)
    phone_no = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(JSON, nullable=True)      
    social_links = Column(JSON, nullable=True)
    legal_details = Column(JSON, nullable=True)

    created_by = Column(String, nullable=True)  
    parent_account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    parent_account = relationship("Account", remote_side=[id], backref="child_accounts")
    # Relationship to leads (which serve as contacts for this account)
    contacts = relationship("Lead", secondary="lead_accounts", back_populates="accounts")
    # Note: leads relationship will be defined in the association table