from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# Base schema - shared fields
class HCPBase(BaseModel):
    name: str
    specialty: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    hospital: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None


# Schema for CREATING a new HCP
class HCPCreate(HCPBase):
    name: str  # Required when creating


# Schema for UPDATING an existing HCP
class HCPUpdate(BaseModel):
    name: Optional[str] = None
    specialty: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    hospital: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    notes: Optional[str] = None


# Schema for READING/RETURNING HCP data
class HCPResponse(HCPBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True