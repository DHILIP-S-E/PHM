# Warehouse Admin Sidebar - Complete Configuration

## ✅ Modules Visible to Warehouse Admin

### 1. 📊 Dashboard
**Path:** `/dashboard`
**Permissions:** `dashboard.view` or `inventory.view.warehouse`
**Purpose:** Overview of warehouse operations, statistics, alerts

---

### 2. 🏢 Warehouses
**Path:** `/warehouses`
**Permissions:** `warehouses.view.warehouse`
**Purpose:** View and manage own warehouse profile
- View warehouse details
- Update warehouse information
- View assigned shops

---

### 3. 📁 Master Data
**Path:** `/master-data`
**Permissions:** See individual sections below
**Purpose:** Manage reference data (CREATE & UPDATE only - NO DELETE)

**Sub-sections:**
- **Categories** - `categories.view`, `categories.create`, `categories.update`
- **Medicine Types** - `medicine_types.view`, `medicine_types.create`, `medicine_types.update`
- **Brands** - `brands.view`, `brands.create`, `brands.update`
- **Manufacturers** - `manufacturers.view`, `manufacturers.create`, `manufacturers.update`
- **Suppliers** - `suppliers.view`, `suppliers.create`, `suppliers.update`
- **Units** - `units.view`, `units.create`, `units.update`
- **HSN Codes** - `hsn.view`, `hsn.create`, `hsn.update`
- **GST Slabs** - `gst.view`, `gst.create`, `gst.update`
- **Departments** - `departments.view`, `departments.create`, `departments.update`
- **Designations** - `designations.view`, `designations.create`, `designations.update`
- **Payment Methods** - `payment_methods.view`, `payment_methods.create`, `payment_methods.update`
- **Adjustment Reasons** - `adjustment_reasons.view`, `adjustment_reasons.create`, `adjustment_reasons.update`

---

### 4. 💊 Medicine Master
**Path:** `/medicines`
**Permissions:** `medicines.view.warehouse`, `medicines.create.warehouse`, `medicines.update.warehouse`
**Purpose:** Manage warehouse medicine catalog
- View all medicines
- Add new medicines
- Update medicine details
- Manage pricing
- View batches

---

### 5. 📦 Inventory Oversight
**Path:** `/inventory` (main section)
**Permissions:** `inventory.view.warehouse`, `inventory.manage.warehouse`
**Purpose:** Complete inventory control

**Sub-sections:**

#### 5a. Stock Entry
**Path:** `/inventory/stock-entry`
**Permissions:** `stock.entry.warehouse`
- Receive new stock shipments
- Create batches
- Record purchase details

#### 5b. Inventory
**Path:** `/inventory/view`
**Permissions:** `inventory.view.warehouse`
- View current stock levels
- Search medicines
- Filter by category/status
- View batch details

#### 5c. Stock Adjustment
**Path:** `/inventory/adjustments`
**Permissions:** `stock.adjust.warehouse`
- Adjust stock for damage
- Mark expired stock
- Reconcile discrepancies
- View adjustment history

---

### 6. 🚚 Dispatches
**Path:** `/dispatches`
**Permissions:** `dispatches.view.warehouse`, `dispatches.create.warehouse`, `dispatches.manage.warehouse`
**Purpose:** Manage shop dispatch orders
- View all dispatches
- Create new dispatches
- Update dispatch status
- Track deliveries
- View dispatch history

---

### 7. 📝 Purchase Requests
**Path:** `/purchase-requests`
**Permissions:** `purchase_requests.view.warehouse`, `purchase_requests.approve`, `purchase_requests.reject`
**Purpose:** Handle shop purchase requests
- View incoming requests
- Approve requests
- Reject requests
- View request history

---

### 8. 👥 Employees
**Path:** `/employees`
**Permissions:** `employees.view.warehouse`, `employees.create.warehouse`, `employees.update.warehouse`
**Purpose:** Warehouse employee management
- View warehouse employees
- Add new employees
- Update employee details
- Manage employee information
- Auto-assign warehouse_id

---

### 9. 📋 Attendance
**Path:** `/attendance`
**Permissions:** `attendance.view.warehouse`, `attendance.manage.warehouse`
**Purpose:** Employee attendance tracking

**Sub-sections:**
- **Attendance Marker** - Mark daily attendance
- **Attendance Report** - View attendance records

---

### 10. 💰 Salary
**Path:** `/salary` or `/payroll`
**Permissions:** `payroll.view.warehouse`, `payroll.process.warehouse`
**Purpose:** Payroll management
- View salary records
- Process salaries
- View payslips
- Manage allowances/deductions

---

### 11. 📊 Reports
**Path:** `/reports`
**Permissions:** `reports.view.warehouse`
**Purpose:** Warehouse performance analytics

**Available Reports:**
- Inventory Reports - `inventory_reports.view.warehouse`
- Dispatch Reports - `dispatch_reports.view.warehouse`
- Sales Summary - `sales_reports.view.warehouse`
- Stock Aging - `inventory.view.warehouse`
- Expiry Report - `expiry.view.warehouse`
- Performance Metrics - `performance_reports.view.warehouse`

---

### 12. 🔔 Notifications
**Path:** `/notifications`
**Permissions:** `notifications.view.warehouse`
**Purpose:** System alerts and notifications
- Low stock alerts - `low_stock_alerts.view`
- Expiry alerts - `expiry_alerts.view`
- Dispatch alerts - `dispatch_alerts.view`
- General notifications

---

## ❌ Modules NOT Visible to Warehouse Admin

### Hidden Sections:
- ❌ **Users & Access** - Platform user management (Super Admin only)
  - Users
  - Roles & Permissions
  - Login Activity
  
- ❌ **Shops** - Individual shop management (unless viewing assigned shops)

- ❌ **Customers** - Shop-level customer management

- ❌ **Invoices** - Shop-level billing (can view shop performance only)

- ❌ **System Settings** - Platform configuration (Super Admin only)

- ❌ **Audit Logs** - Full audit trail (Super Admin only)

---

## 🔐 Permission Summary

### Warehouse Admin Has:
✅ **VIEW** - All warehouse data
✅ **CREATE** - Inventory, employees, dispatches, master data
✅ **UPDATE** - Inventory, employees, dispatches, master data
✅ **APPROVE/REJECT** - Purchase requests
❌ **DELETE** - Master data (cannot delete reference data)
❌ **PLATFORM ADMIN** - No platform-level access

### Scope:
- **Warehouse-scoped** - Only their assigned warehouse
- **Auto-filtered** - All queries filter by `warehouse_id`
- **Entity-isolated** - Cannot see other warehouses' data

---

## 📱 Sidebar Implementation

### Sidebar Structure (operationalItems):
```typescript
const operationalItems = [
  {
    path: '/dashboard',
    label: 'Dashboard',
    icon: 'dashboard',
    permissions: ['dashboard.view', 'inventory.view.warehouse']
  },
  {
    path: '/warehouses',
    label: 'Warehouses',
    icon: 'warehouse',
    permissions: ['warehouses.view', 'warehouses.view.warehouse']
  },
  {
    path: '/master-data',
    label: 'Master Data',
    icon: 'settings',
    permissions: ['categories.view', 'brands.view', 'manufacturers.view'],
    children: [...]
  },
  {
    path: '/medicines',
    label: 'Medicine Master',
    icon: 'medication',
    permissions: ['medicines.view', 'medicines.view.warehouse']
  },
  {
    path: '/inventory',
    label: 'Inventory Oversight',
    icon: 'inventory',
    permissions: ['inventory.view.warehouse'],
    children: [
      { path: '/inventory/stock-entry', label: 'Stock Entry', permissions: ['stock.entry.warehouse'] },
      { path: '/inventory/view', label: 'Inventory', permissions: ['inventory.view.warehouse'] },
      { path: '/inventory/adjustments', label: 'Stock Adjustment', permissions: ['stock.adjust.warehouse'] }
    ]
  },
  {
    path: '/dispatches',
    label: 'Dispatches',
    icon: 'local_shipping',
    permissions: ['dispatches.view.warehouse', 'dispatches.view']
  },
  {
    path: '/purchase-requests',
    label: 'Purchase Requests',
    icon: 'shopping_cart',
    permissions: ['purchase_requests.view.warehouse', 'purchase_requests.view']
  },
  {
    path: '/employees',
    label: 'Employees',
    icon: 'people',
    permissions: ['employees.view.warehouse', 'employees.view']
  },
  {
    path: '/attendance',
    label: 'Attendance',
    icon: 'event_available',
    permissions: ['attendance.view.warehouse', 'attendance.manage.warehouse'],
    children: [
      { path: '/attendance/marker', label: 'Attendance Marker' },
      { path: '/attendance/report', label: 'Attendance Report' }
    ]
  },
  {
    path: '/salary',
    label: 'Salary',
    icon: 'payments',
    permissions: ['payroll.view.warehouse', 'payroll.view']
  },
  {
    path: '/reports',
    label: 'Reports',
    icon: 'assessment',
    permissions: ['reports.view.warehouse', 'reports.view']
  },
  {
    path: '/notifications',
    label: 'Notifications',
    icon: 'notifications',
    permissions: ['notifications.view.warehouse', 'notifications.view']
  }
];
```

---

## ✅ Verification Checklist

When logged in as Warehouse Admin, verify:
- [ ] Can see Dashboard
- [ ] Can see Warehouses (own warehouse only)
- [ ] Can see Master Data with CREATE/UPDATE (no DELETE)
- [ ] Can see Medicine Master
- [ ] Can see Inventory section with sub-items
- [ ] Can see Dispatches
- [ ] Can see Purchase Requests
- [ ] Can see Employees (can create warehouse employees)
- [ ] Can see Attendance (Marker + Report)
- [ ] Can see Salary/Payroll
- [ ] Can see Reports (warehouse reports only)
- [ ] Can see Notifications
- [ ] **CANNOT** see Users & Access
- [ ] **CANNOT** see Shops (main management)
- [ ] **CANNOT** see Customers
- [ ] **CANNOT** see Invoices
- [ ] **CANNOT** see System Settings
- [ ] All data filtered by warehouse_id automatically

---

## 📚 Related Documentation
- Full Permissions: `.agent/WAREHOUSE_ADMIN_PERMISSIONS.md`
- Sidebar Code: `src/components/Sidebar.tsx`
- User Management: `WAREHOUSE_ADMIN_USER_MANAGEMENT.md` (if exists)
