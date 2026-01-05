"""
Customer and CRM schemas
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class CustomerType(str, Enum):
    REGULAR = "regular"
    VIP = "vip"
    CORPORATE = "corporate"
    INSURANCE = "insurance"


class FollowupStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# Customer
class CustomerBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    customer_type: CustomerType = CustomerType.REGULAR
    notes: Optional[str] = None


class CustomerCreate(CustomerBase):
    shop_id: str


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    customer_type: Optional[CustomerType] = None
    notes: Optional[str] = None


class CustomerResponse(CustomerBase):
    id: str
    shop_id: str
    total_purchases: int = 0
    total_spent: float = 0.0
    loyalty_points: int = 0
    last_visit: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class CustomerListResponse(BaseModel):
    items: list[CustomerResponse]
    total: int
    page: int
    size: int


# Follow-up
class FollowupBase(BaseModel):
    customer_id: str
    followup_date: date
    reason: str
    notes: Optional[str] = None


class FollowupCreate(FollowupBase):
    pass


class FollowupResponse(FollowupBase):
    id: str
    status: FollowupStatus
    completed_at: Optional[datetime] = None
    created_by: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Prescription
class PrescriptionBase(BaseModel):
    customer_id: str
    doctor_name: str
    hospital_name: Optional[str] = None
    prescription_date: date
    notes: Optional[str] = None
    image_url: Optional[str] = None


class PrescriptionCreate(PrescriptionBase):
    pass


class PrescriptionResponse(PrescriptionBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
