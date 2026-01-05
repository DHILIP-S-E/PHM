"""
Warehouse schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class WarehouseStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


class WarehouseBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=20)
    address: str
    city: str
    state: str
    country: str = "India"
    pincode: str
    phone: Optional[str] = None
    email: Optional[str] = None
    manager_id: Optional[str] = None
    capacity: Optional[int] = None
    status: WarehouseStatus = WarehouseStatus.ACTIVE


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    manager_id: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[WarehouseStatus] = None


class WarehouseResponse(WarehouseBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    shop_count: int = 0
    total_stock_value: float = 0.0

    class Config:
        from_attributes = True


class WarehouseListResponse(BaseModel):
    items: list[WarehouseResponse]
    total: int
    page: int
    size: int


class WarehouseShopMapping(BaseModel):
    warehouse_id: str
    shop_id: str
    is_primary: bool = True
