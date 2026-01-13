# Complete Module & Permission Mapping for PHM System

## All Modules in the System

Based on the codebase analysis, here are ALL modules that should have permissions:

### ✅ Already Defined in permissions.ts

1. **Dashboard** - `dashboard.view`
2. **Users** - `users.view`, `users.create`, `users.edit`, `users.delete`
3. **Roles & Permissions** - `roles.view`, `roles.manage`
4. **Warehouses** - `warehouses.view`, `warehouses.create`, `warehouses.edit`, `warehouses.delete`
5. **Medical Shops** - `shops.view`, `shops.create`, `shops.edit`, `shops.delete`
6. **Medicines** - `medicines.view`, `medicines.create`, `medicines.edit`, `medicines.delete`
7. **Categories** - `categories.manage`
8. **Units** - `units.manage`
9. **HSN Codes** - `hsn.manage`
10. **GST Slabs** - `gst.manage`
11. **Inventory** - `inventory.view.global`, `inventory.view.warehouse`, `inventory.view.shop`, `inventory.oversight`, `inventory.adjust.warehouse`, `inventory.adjust.shop`, `inventory.entry.warehouse`
12. **Racks** - `racks.view`, `racks.manage.warehouse`
13. **Purchase Requests** - `purchase_requests.view.global`, `purchase_requests.view.warehouse`, `purchase_requests.view.shop`, `purchase_requests.create.shop`, `purchase_requests.approve.warehouse`
14. **Dispatches** - `dispatches.view.global`, `dispatches.view.warehouse`, `dispatches.view.shop`, `dispatches.create.warehouse`
15. **Billing/POS** - `billing.view.shop`, `billing.create.shop`, `billing.void.shop`
16. **Returns** - `returns.view.shop`, `returns.create.shop`
17. **Customers** - `customers.view`, `customers.view.shop`, `customers.manage.shop`
18. **Employees** - `employees.view.global`, `employees.view.warehouse`, `employees.view.shop`, `employees.manage.warehouse`, `employees.manage.shop`
19. **Attendance** - `attendance.manage.warehouse`, `attendance.manage.shop`
20. **Salary** - `salary.manage.warehouse`, `salary.manage.shop`
21. **Reports** - `reports.view.global`, `reports.view.warehouse`, `reports.view.shop`, `reports.export`
22. **Settings** - `settings.view`, `settings.manage`
23. **Audit Logs** - `audit.view`
24. **Login Activity** - `login_activity.view`
25. **Notifications** - `notifications.view`

### ❌ MISSING Permissions (Need to be Added)

26. **Brands** (Master Data)
    - `brands.view`
    - `brands.create`
    - `brands.edit`
    - `brands.delete`

27. **Manufacturers** (Master Data)
    - `manufacturers.view`
    - `manufacturers.create`
    - `manufacturers.edit`
    - `manufacturers.delete`

28. **Medicine Types** (Master Data)
    - `medicine_types.view`
    - `medicine_types.create`
    - `medicine_types.edit`
    - `medicine_types.delete`

29. **Suppliers** (Master Data)
    - `suppliers.view`
    - `suppliers.create`
    - `suppliers.edit`
    - `suppliers.delete`

30. **Adjustment Reasons** (Master Data)
    - `adjustment_reasons.view`
    - `adjustment_reasons.create`
    - `adjustment_reasons.edit`
    - `adjustment_reasons.delete`

31. **Payment Methods** (Master Data)
    - `payment_methods.view`
    - `payment_methods.create`
    - `payment_methods.edit`
    - `payment_methods.delete`

32. **Shop Types** (Master Data) - Currently hardcoded, but if made dynamic:
    - `shop_types.view`
    - `shop_types.create`
    - `shop_types.edit`
    - `shop_types.delete`

33. **Customer Types** (Master Data)
    - `customer_types.view`
    - `customer_types.create`
    - `customer_types.edit`
    - `customer_types.delete`

34. **Genders** (Master Data)
    - `genders.view`
    - `genders.manage`

35. **Employment Types** (Master Data)
    - `employment_types.view`
    - `employment_types.manage`

36. **Urgency Levels** (Master Data)
    - `urgency_levels.view`
    - `urgency_levels.manage`

37. **Statuses** (Master Data)
    - `statuses.view`
    - `statuses.manage`

38. **Designations** (Master Data)
    - `designations.view`
    - `designations.create`
    - `designations.edit`
    - `designations.delete`

39. **Departments** (Master Data)
    - `departments.view`
    - `departments.create`
    - `departments.edit`
    - `departments.delete`

## Recommended Action

Add all missing master data permissions to:
1. **Backend**: `backend/scripts/seed_permissions.py` or migration
2. **Frontend**: `src/types/permissions.ts` PERMISSIONS constant

## Permission Naming Convention

Follow this pattern:
- **View**: `module.view` or `module.view.scope`
- **Create**: `module.create` or `module.create.scope`
- **Edit/Update**: `module.edit` or `module.update.scope`
- **Delete**: `module.delete` or `module.delete.scope`
- **Manage** (all CRUD): `module.manage` or `module.manage.scope`

Where `scope` can be: `global`, `warehouse`, or `shop`
