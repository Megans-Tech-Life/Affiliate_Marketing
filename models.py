import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Table, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base

# Many-to-Many relationship between Leads and Accounts
lead_accounts = Table(
    "lead_accounts",
    Base.metadata,
    Column("lead_id", UUID(as_uuid=True), ForeignKey("leads.id")),
    Column("account_id", UUID(as_uuid=True), ForeignKey("accounts.id"))
)

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
    contacts = relationship("Contact", back_populates="account")
    leads = relationship("Lead", secondary="lead_accounts", back_populates="accounts")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(255), nullable=True)
    phone_code = Column(String(10), nullable=True)
    phone_no = Column(String(20), nullable=True)
    entry_point = Column(String(20), default="INDV")
    social_links = Column(JSON, nullable=True)
    address = Column(JSON, nullable=True)

    created_by = Column(String, nullable=True)   # affiliate_user_id
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    account = relationship("Account", back_populates="contacts")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255), nullable=True)
    phone_code = Column(String(10), nullable=True)
    phone_no = Column(String(20), nullable=True)
    entry_point = Column(String(20), default="INDV")
    platform = Column(String(255), nullable=True)

    lead_stage = Column(String, nullable=True)  
    created_by = Column(String, nullable=True)  # affiliate_user_id

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    accounts = relationship("Account", secondary=lead_accounts, back_populates="leads")
    details = relationship("LeadDetails", uselist=False, back_populates="lead")
    notes = relationship("LeadNote", back_populates="lead")
    products = relationship("LeadProduct", back_populates="lead")

class LeadDetails(Base):
    __tablename__ = "lead_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"))
    dob = Column(DateTime, nullable=True)
    gender = Column(String(20), nullable=True)
    marital_status = Column(String(50), nullable=True)
    children = Column(Integer, nullable=True)
    occupation = Column(String(100), nullable=True)
    legal_details = Column(String(50), nullable=True)
    social_links = Column(JSON, nullable=True)
    addresses = Column(JSON, nullable=True)
    notes = Column(Text, nullable=True)

    lead = relationship("Lead", back_populates="details")

class LeadNote(Base):
    __tablename__ = "lead_notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"))
    note = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user_id = Column(String, nullable=True)  # affiliate_user_id
    lead = relationship("Lead", back_populates="notes")


class LeadProduct(Base):
    __tablename__ = "lead_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"))
    product = Column(String, nullable=False)   # simplify: store product name or ID
    interest_level = Column(String(50), nullable=True)

    lead = relationship("Lead", back_populates="products")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))