"""
API v1 Router - Aggregates all route modules
"""
from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.warehouses import router as warehouses_router
from app.api.v1.shops import router as shops_router
from app.api.v1.medicines import router as medicines_router
from app.api.v1.inventory import router as inventory_router
from app.api.v1.purchase_requests import router as purchase_requests_router
from app.api.v1.dispatches import router as dispatches_router
from app.api.v1.invoices import router as invoices_router
from app.api.v1.customers import router as customers_router
from app.api.v1.employees import router as employees_router
from app.api.v1.reports import router as reports_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.settings import router as settings_router
from app.api.v1.roles import router as roles_router
from app.api.v1.tax import router as tax_router

router = APIRouter()

# Mount all routers
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(users_router, prefix="/users", tags=["Users"])
router.include_router(roles_router, prefix="/roles", tags=["Roles"])
router.include_router(warehouses_router, prefix="/warehouses", tags=["Warehouses"])
router.include_router(shops_router, prefix="/shops", tags=["Medical Shops"])
router.include_router(medicines_router, prefix="/medicines", tags=["Medicines"])
router.include_router(inventory_router, prefix="/stock", tags=["Inventory"])
router.include_router(purchase_requests_router, prefix="/purchase-requests", tags=["Purchase Requests"])
router.include_router(dispatches_router, prefix="/dispatches", tags=["Dispatches"])
router.include_router(invoices_router, prefix="/invoices", tags=["Invoices"])
router.include_router(customers_router, prefix="/customers", tags=["Customers"])
router.include_router(employees_router, prefix="/employees", tags=["Employees"])
router.include_router(reports_router, prefix="/reports", tags=["Reports"])
router.include_router(notifications_router, prefix="/notifications", tags=["Notifications"])
router.include_router(settings_router, prefix="/settings", tags=["Settings"])
router.include_router(tax_router, prefix="/tax", tags=["Tax & Accounting"])
