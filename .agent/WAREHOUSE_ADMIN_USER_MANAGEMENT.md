# Warehouse Admin - User Management Capabilities

## 🔐 User Management Scope

### ✅ What Warehouse Admin CAN Do:

#### 1. **View Users (Warehouse-Scoped)**
- Permission: `users.view.warehouse`
- Can view all users assigned to their warehouse
- See user details: name, email, phone, role, status
- View user activity and last login
- ❌ Cannot view users from other warehouses

#### 2. **Create Users (Warehouse-Scoped)**
- Permission: `users.create.warehouse`
- Can create new user accounts for their warehouse
- **Allowed Roles to Assign:**
  - ✅ `warehouse_employee` - Regular warehouse staff
  - ✅ `warehouse_supervisor` - Warehouse supervisors  
  - ✅ `inventory_manager` - Inventory managers
  - ✅ `warehouse_clerk` - Warehouse clerks
- **Restricted Roles (Cannot Assign):**
  - ❌ `warehouse_admin` - Only Super Admin can create
  - ❌ `super_admin` - System role, cannot be assigned
  - ❌ `pharmacy_admin` - Shop-level role
  - ❌ `pharmacist` - Shop-level role

#### 3. **Update Users (Warehouse-Scoped)**
- Permission: `users.update.warehouse`
- Can update user details:
  - ✅ Full name
  - ✅ Email address
  - ✅ Phone number
  - ✅ Change role (within allowed roles)
  - ✅ Activate/deactivate user
- ❌ Cannot update users from other warehouses
- ❌ Cannot change their own role

#### 4. **Delete/Deactivate Users (Warehouse-Scoped)**
- Permission: `users.delete.warehouse`
- Can soft-delete (deactivate) users
- User account is not permanently deleted, just marked inactive
- ❌ Cannot delete themselves
- ❌ Cannot delete users from other warehouses

---

## 🔒 Security & Restrictions

### Entity Scope Enforcement:
```
Warehouse Admin (Warehouse ID: ABC-123)
  ↓
Can ONLY manage users where:
  - user.assigned_warehouse_id == "ABC-123"
  
Cannot access users where:
  - user.assigned_warehouse_id != "ABC-123"
  - user.assigned_warehouse_id == null (global users)
```

### Role Assignment Rules:
```
✅ ALLOWED ROLES:
- warehouse_employee
- warehouse_supervisor
- inventory_manager
- warehouse_clerk

❌ RESTRICTED ROLES:
- warehouse_admin (requires Super Admin)
- super_admin (system role)
- pharmacy_admin (shop-level)
- pharmacist (shop-level)
- cashier (shop-level)
```

---

## 📋 User Management Workflow

### Creating a New Warehouse User:

1. **Navigate to Users Page**
   - Sidebar → User Management
   - Click "Add User"

2. **Fill User Details**
   - Full Name: `John Doe`
   - Email: `john.doe@warehouse.com`
   - Phone: `+91 9876543210`
   - Role: Select from dropdown (only allowed roles shown)
   - Warehouse: Auto-filled (their warehouse)
   - Password: Set initial password

3. **User is Created**
   - User receives email with credentials
   - User is assigned to the warehouse
   - User can log in with warehouse-scoped access

### Updating a User:

1. **Find User in List**
   - Search by name or email
   - Click "Edit" button

2. **Modify Details**
   - Update name, email, phone
   - Change role (if needed)
   - Activate/deactivate

3. **Save Changes**
   - User is updated
   - If role changed, permissions update automatically

### Deactivating a User:

1. **Select User**
   - Find user in list
   - Click "Delete" button

2. **Confirm Deactivation**
   - User is marked as inactive
   - User cannot log in
   - User data is preserved (not deleted)

---

## 🎯 Use Cases

### Use Case 1: Onboarding New Warehouse Staff
```
Scenario: New employee joins warehouse
Action: Warehouse Admin creates user account
Role: warehouse_employee
Result: Employee can log in and access warehouse features
```

### Use Case 2: Promoting Warehouse Employee
```
Scenario: Employee promoted to supervisor
Action: Warehouse Admin updates user role
Role: warehouse_employee → warehouse_supervisor
Result: User gets supervisor-level permissions
```

### Use Case 3: Employee Leaves Company
```
Scenario: Employee resigns
Action: Warehouse Admin deactivates user
Result: User cannot log in, data preserved for audit
```

---

## 🚫 What Warehouse Admin CANNOT Do

### Platform Administration:
- ❌ Create Super Admin users
- ❌ Create Warehouse Admin users
- ❌ Manage roles or permissions
- ❌ Access global user list
- ❌ Modify system settings

### Cross-Warehouse Access:
- ❌ View users from other warehouses
- ❌ Create users for other warehouses
- ❌ Transfer users between warehouses
- ❌ Access warehouse admin users

### Shop-Level Users:
- ❌ Create pharmacy/shop users
- ❌ Assign shop-level roles
- ❌ Manage shop staff

---

## 📊 Summary

**Total User Management Permissions: 4**
- `users.view.warehouse` - View warehouse users
- `users.create.warehouse` - Create warehouse users
- `users.update.warehouse` - Update warehouse users
- `users.delete.warehouse` - Deactivate warehouse users

**Scope:** Warehouse-level only
**Allowed Roles:** 4 warehouse-level roles
**Restrictions:** Cannot access other warehouses or assign admin roles
