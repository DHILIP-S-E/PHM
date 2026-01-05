"""
Inventory & Stock API Routes - Database Connected
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from datetime import date, timedelta
from pydantic import BaseModel

from app.models.common import APIResponse
from app.core.security import get_current_user, require_role
from app.db.database import get_db
from app.db.models import Batch, Medicine

router = APIRouter()


class StockAdjustment(BaseModel):
    medicine_id: str
    batch_id: str
    adjustment_type: str  # increase, decrease
    quantity: int
    reason: str


@router.get("/movements")
async def get_stock_movements(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    location_type: Optional[str] = None,
    location_id: Optional[str] = None,
    movement_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get stock movements history"""
    # For now, return empty since we don't have a movements table yet
    return {
        "movements": [],
        "total": 0,
        "page": page,
        "size": size
    }


@router.post("/adjust")
async def adjust_stock(
    adjustment: StockAdjustment,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role(["super_admin", "warehouse_admin"]))
):
    """Adjust stock quantity for a batch"""
    batch = db.query(Batch).filter(Batch.id == adjustment.batch_id).first()
    if not batch:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Batch not found")
    
    if adjustment.adjustment_type == "increase":
        batch.quantity = (batch.quantity or 0) + adjustment.quantity
    elif adjustment.adjustment_type == "decrease":
        new_qty = (batch.quantity or 0) - adjustment.quantity
        if new_qty < 0:
            from fastapi import HTTPException
            raise HTTPException(status_code=400, detail="Cannot reduce stock below zero")
        batch.quantity = new_qty
    
    db.commit()
    
    return APIResponse(message="Stock adjusted successfully", data={"new_quantity": batch.quantity})


@router.get("/alerts")
async def get_stock_alerts(
    alert_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get stock alerts (low stock, expiring, expired)"""
    today = date.today()
    expiry_warning_days = 60
    low_stock_threshold = 50
    
    alerts = []
    
    # Get low stock items
    if not alert_type or alert_type == "low_stock":
        batches = db.query(Batch).join(Medicine).filter(
            Batch.quantity <= low_stock_threshold,
            Batch.quantity > 0,
            Batch.expiry_date > today
        ).all()
        
        for batch in batches:
            medicine = db.query(Medicine).filter(Medicine.id == batch.medicine_id).first()
            alerts.append({
                "id": f"low_{batch.id}",
                "type": "low_stock",
                "medicine_id": batch.medicine_id,
                "medicine_name": medicine.name if medicine else "Unknown",
                "batch_number": batch.batch_number,
                "current_quantity": batch.quantity,
                "threshold": low_stock_threshold,
                "created_at": batch.created_at
            })
    
    # Get expiring items
    if not alert_type or alert_type == "expiring":
        future_date = today + timedelta(days=expiry_warning_days)
        batches = db.query(Batch).join(Medicine).filter(
            Batch.expiry_date >= today,
            Batch.expiry_date <= future_date,
            Batch.quantity > 0
        ).all()
        
        for batch in batches:
            medicine = db.query(Medicine).filter(Medicine.id == batch.medicine_id).first()
            days_to_expiry = (batch.expiry_date - today).days if batch.expiry_date else 0
            alerts.append({
                "id": f"exp_{batch.id}",
                "type": "expiring",
                "medicine_id": batch.medicine_id,
                "medicine_name": medicine.name if medicine else "Unknown",
                "batch_number": batch.batch_number,
                "expiry_date": batch.expiry_date.isoformat() if batch.expiry_date else None,
                "days_to_expiry": days_to_expiry,
                "quantity": batch.quantity,
                "created_at": batch.created_at
            })
    
    # Get expired items
    if not alert_type or alert_type == "expired":
        batches = db.query(Batch).join(Medicine).filter(
            Batch.expiry_date < today,
            Batch.quantity > 0
        ).all()
        
        for batch in batches:
            medicine = db.query(Medicine).filter(Medicine.id == batch.medicine_id).first()
            alerts.append({
                "id": f"expd_{batch.id}",
                "type": "expired",
                "medicine_id": batch.medicine_id,
                "medicine_name": medicine.name if medicine else "Unknown",
                "batch_number": batch.batch_number,
                "expiry_date": batch.expiry_date.isoformat() if batch.expiry_date else None,
                "quantity": batch.quantity,
                "created_at": batch.created_at
            })
    
    return {"alerts": alerts, "total": len(alerts)}
