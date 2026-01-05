"""
Inventory and Stock schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum


class StockMovementType(str, Enum):
    IN = "in"
    OUT = "out"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"
    RETURN = "return"
    EXPIRED = "expired"


# Warehouse Stock
class WarehouseStockBase(BaseModel):
    warehouse_id: str
    medicine_id: str
    batch_id: str
    quantity: int = Field(ge=0)
    reorder_level: int = 10
    max_stock: int = 1000
    rack_location: Optional[str] = None
    shelf_number: Optional[str] = None


class WarehouseStockCreate(WarehouseStockBase):
    pass


class WarehouseStockUpdate(BaseModel):
    quantity: Optional[int] = None
    reorder_level: Optional[int] = None
    max_stock: Optional[int] = None
    rack_location: Optional[str] = None
    shelf_number: Optional[str] = None


class WarehouseStockResponse(WarehouseStockBase):
    id: str
    medicine_name: Optional[str] = None
    batch_number: Optional[str] = None
    expiry_date: Optional[datetime] = None
    stock_value: float = 0.0
    is_low_stock: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Shop Stock
class ShopStockBase(BaseModel):
    shop_id: str
    medicine_id: str
    batch_id: str
    quantity: int = Field(ge=0)
    reorder_level: int = 5
    rack_location: Optional[str] = None


class ShopStockResponse(ShopStockBase):
    id: str
    medicine_name: Optional[str] = None
    batch_number: Optional[str] = None
    expiry_date: Optional[datetime] = None
    mrp: float = 0.0
    stock_value: float = 0.0
    is_low_stock: bool = False

    class Config:
        from_attributes = True


# Stock Movement
class StockMovementBase(BaseModel):
    medicine_id: str
    batch_id: str
    movement_type: StockMovementType
    quantity: int
    from_location_type: Optional[str] = None
    from_location_id: Optional[str] = None
    to_location_type: Optional[str] = None
    to_location_id: Optional[str] = None
    reference_type: Optional[str] = None
    reference_id: Optional[str] = None
    notes: Optional[str] = None


class StockMovementCreate(StockMovementBase):
    pass


class StockMovementResponse(StockMovementBase):
    id: str
    medicine_name: Optional[str] = None
    performed_by: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Stock Adjustment
class StockAdjustmentRequest(BaseModel):
    location_type: str  # warehouse or shop
    location_id: str
    medicine_id: str
    batch_id: str
    adjustment_quantity: int  # can be positive or negative
    reason: str
    notes: Optional[str] = None


class StockThreshold(BaseModel):
    medicine_id: str
    location_type: str
    location_id: str
    min_threshold: int = 10
    max_threshold: int = 1000
    auto_reorder: bool = False
