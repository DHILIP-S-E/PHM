# Warehouse Admin - Complete Permission Set

## Overview
Warehouse Admin manages warehouse operations, NOT the platform itself.
This role has **warehouse-scoped permissions** for operational management.

---

## 🔐 USER MANAGEMENT (WAREHOUSE-SCOPED)
**Purpose:** Manage users within their warehouse only

### Permissions:
- `users.view.warehouse` - View users in their warehouse
- `users.create.warehouse` - Create users for their warehouse
- `users.update.warehouse` - Update users in their warehouse
- `users.delete.warehouse` - Deactivate users in their warehouse

### Allowed Roles to Assign:
- ✅ `warehouse_employee` - Regular warehouse staff
- ✅ `warehouse_supervisor` - Warehouse supervisors
- ✅ `inventory_manager` - Inventory managers
- ✅ `warehouse_clerk` - Warehouse clerks

### Restricted Roles (Cannot Assign):
- ❌ `warehouse_admin` - Only Super Admin can create
- ❌ `super_admin` - System role
- ❌ Shop-level roles (pharmacy_admin, pharmacist, cashier)

**Note:** See `WAREHOUSE_ADMIN_USER_MANAGEMENT.md` for detailed workflows.

---

## 1️⃣ WAREHOUSE MANAGEMENT
**Purpose:** Manage warehouse profile and staff

### Permissions:
- `warehouses.view.warehouse` - View own warehouse profile
- `warehouses.update.warehouse` - Update warehouse details
- `warehouse_staff.view` - View warehouse staff
- `warehouse_staff.manage` - Manage warehouse employees
- `shops.view.warehouse` - View assigned medical shops

---

## 2️⃣ INVENTORY MANAGEMENT
**Purpose:** Complete warehouse inventory control

### Permissions:
- `inventory.view.warehouse` - View warehouse inventory
- `inventory.manage.warehouse` - Full inventory management
- `stock.entry.warehouse` - Add new stock (receive shipments)
- `stock.adjust.warehouse` - Adjust stock levels (damage, expiry)
- `stock.transfer.warehouse` - Transfer stock between warehouses
- `batches.view.warehouse` - View batch information
- `batches.manage.warehouse` - Manage batch details
- `expiry.view.warehouse` - View expiry tracking
- `expiry.manage.warehouse` - Manage expiry alerts
- `stock_alerts.view.warehouse` - View low stock alerts
- `stock_alerts.manage.warehouse` - Configure stock thresholds

---

## 3️⃣ PURCHASE & DISPATCH
**Purpose:** Handle shop purchase requests and dispatch orders

### Permissions:
- `purchase_requests.view.warehouse` - View shop purchase requests
- `purchase_requests.approve` - Approve purchase requests
- `purchase_requests.reject` - Reject purchase requests
- `dispatches.view.warehouse` - View dispatch orders
- `dispatches.create.warehouse` - Create new dispatches
- `dispatches.update.warehouse` - Update dispatch status
- `dispatches.manage.warehouse` - Full dispatch management

---

## 4️⃣ MEDICINE CATALOG (LIMITED)
**Purpose:** Manage warehouse-specific medicine catalog

### Permissions:
- `medicines.view.warehouse` - View medicine catalog
- `medicines.create.warehouse` - Add local medicines
- `medicines.update.warehouse` - Update medicine details
- `medicine_pricing.manage.warehouse` - Manage pricing

---

## 5️⃣ SHOP OVERSIGHT
**Purpose:** Monitor assigned shop performance

### Permissions:
- `shops.view.warehouse` - View assigned shops
- `shop_performance.view` - View shop sales performance
- `shop_inventory.view` - View shop inventory levels
- `shop_analytics.view` - View shop analytics

---

## 6️⃣ TAX & ACCOUNTING
**Purpose:** Warehouse tax and financial reports

### Permissions:
- `gst_reports.view.warehouse` - View GST reports
- `tax_reports.view.warehouse` - View tax reports
- `purchase_tax.view.warehouse` - View purchase tax details
- `returns.view.warehouse` - View product returns
- `returns.manage.warehouse` - Process returns

---

## 7️⃣ REPORTS & ANALYTICS
**Purpose:** Warehouse performance and analytics

### Permissions:
- `reports.view.warehouse` - View warehouse reports
- `analytics.view.warehouse` - View analytics dashboard
- `sales_reports.view.warehouse` - View sales summary
- `dispatch_reports.view.warehouse` - View dispatch performance
- `inventory_reports.view.warehouse` - View inventory aging
- `performance_reports.view.warehouse` - View performance metrics

---

## 8️⃣ HR MANAGEMENT
**Purpose:** Warehouse employee management

### Permissions:
- `employees.view.warehouse` - View warehouse employees
- `employees.create.warehouse` - Add new employees
- `employees.update.warehouse` - Update employee details
- `attendance.view.warehouse` - View attendance records
- `attendance.manage.warehouse` - Mark attendance
- `payroll.view.warehouse` - View payroll information
- `payroll.process.warehouse` - Process payroll
- `leave.view.warehouse` - View leave requests
- `leave.manage.warehouse` - Approve/reject leave

---

## 9️⃣ NOTIFICATIONS & ALERTS
**Purpose:** Operational alerts and notifications

### Permissions:
- `notifications.view.warehouse` - View notifications
- `alerts.view.warehouse` - View system alerts
- `low_stock_alerts.view` - View low stock alerts
- `expiry_alerts.view` - View expiry alerts
- `dispatch_alerts.view` - View dispatch alerts

---

## 🔍 MASTER DATA (CREATE & UPDATE - NO DELETE)
**Purpose:** Manage reference data for warehouse operations

### Permissions:
**Categories:**
- `categories.view` - View medicine categories
- `categories.create` - Create new categories
- `categories.update` - Update categories
- ❌ NO DELETE permission

**Units:**
- `units.view` - View units/packaging
- `units.create` - Create new units
- `units.update` - Update units
- ❌ NO DELETE permission

**Brands:**
- `brands.view` - View brands
- `brands.create` - Create new brands
- `brands.update` - Update brands
- ❌ NO DELETE permission

**Manufacturers:**
- `manufacturers.view` - View manufacturers
- `manufacturers.create` - Create new manufacturers
- `manufacturers.update` - Update manufacturers
- ❌ NO DELETE permission

**Medicine Types:**
- `medicine_types.view` - View medicine types
- `medicine_types.create` - Create new medicine types
- `medicine_types.update` - Update medicine types
- ❌ NO DELETE permission

**HSN Codes:**
- `hsn.view` - View HSN codes
- `hsn.create` - Create new HSN codes
- `hsn.update` - Update HSN codes
- ❌ NO DELETE permission

**GST Slabs:**
- `gst.view` - View GST slabs
- `gst.create` - Create new GST slabs
- `gst.update` - Update GST slabs
- ❌ NO DELETE permission

**Suppliers:**
- `suppliers.view` - View suppliers
- `suppliers.create` - Create new suppliers
- `suppliers.update` - Update suppliers
- ❌ NO DELETE permission

**Payment Methods:**
- `payment_methods.view` - View payment methods
- `payment_methods.create` - Create new payment methods
- `payment_methods.update` - Update payment methods
- ❌ NO DELETE permission

**Adjustment Reasons:**
- `adjustment_reasons.view` - View adjustment reasons
- `adjustment_reasons.create` - Create new adjustment reasons
- `adjustment_reasons.update` - Update adjustment reasons
- ❌ NO DELETE permission

**Racks:**
- `racks.view` - View rack master
- `racks.create` - Create new racks
- `racks.update` - Update racks
- `racks.manage.warehouse` - Manage warehouse racks
- ❌ NO DELETE permission

---

## 📊 Total Permissions: 120+

### Permission Scope:
- **Warehouse-scoped:** Most permissions (can only access their assigned warehouse)
- **Master data:** Can CREATE and UPDATE, but CANNOT DELETE
- **No platform admin:** Cannot manage users, roles, or system settings

### Key Restrictions:
❌ Cannot create/modify USERS with ROLES (only warehouse employees)
❌ Cannot manage roles or permissions
❌ Cannot DELETE master data (categories, units, brands, etc.)
❌ Cannot access other warehouses
❌ Cannot access Super Admin functions

### Operational Focus:
✅ Full warehouse inventory control
✅ Shop purchase request approval
✅ Dispatch order management
✅ Warehouse employee management (NOT user accounts)
✅ Master data creation and updates (NO deletion)
✅ Performance monitoring
✅ Tax and compliance reports
