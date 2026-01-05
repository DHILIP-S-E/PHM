"""
Common Pydantic models and schemas
"""
from datetime import datetime
from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common configuration"""
    
    class Config:
        from_attributes = True
        populate_by_name = True


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper"""
    items: list[T]
    total: int
    page: int
    size: int
    pages: int


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper"""
    success: bool = True
    message: str = "Success"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    message: str
    detail: Optional[str] = None
    error_code: Optional[str] = None


class StatusEnum(BaseModel):
    """Common status values"""
    ACTIVE: str = "active"
    INACTIVE: str = "inactive"
    PENDING: str = "pending"
    DELETED: str = "deleted"
