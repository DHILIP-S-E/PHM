/**
 * Role-Based Access Control Utilities
 */

export const Permissions = {
    // Warehouses
    WAREHOUSE_CREATE: ['super_admin', 'warehouse_admin'],
    WAREHOUSE_UPDATE: ['super_admin', 'warehouse_admin'],
    WAREHOUSE_DELETE: ['super_admin'],
    WAREHOUSE_VIEW: ['super_admin', 'warehouse_admin', 'shop_owner', 'pharmacist'],

    // Shops
    SHOP_CREATE: ['super_admin', 'warehouse_admin'],
    SHOP_UPDATE: ['super_admin', 'warehouse_admin', 'shop_owner'],
    SHOP_DELETE: ['super_admin'],
    SHOP_VIEW: ['super_admin', 'warehouse_admin', 'shop_owner', 'pharmacist'],

    // Medicines
    MEDICINE_CREATE: ['super_admin', 'warehouse_admin'],
    MEDICINE_UPDATE: ['super_admin', 'warehouse_admin'],
    MEDICINE_DELETE: ['super_admin'],
    MEDICINE_VIEW: ['super_admin', 'warehouse_admin', 'shop_owner', 'pharmacist', 'cashier'],

    // Users
    USER_CREATE: ['super_admin'],
    USER_UPDATE: ['super_admin'],
    USER_DELETE: ['super_admin'],
    USER_VIEW: ['super_admin'],

    // Employees
    EMPLOYEE_CREATE: ['super_admin', 'hr_manager'],
    EMPLOYEE_UPDATE: ['super_admin', 'hr_manager'],
    EMPLOYEE_DELETE: ['super_admin', 'hr_manager'],
    EMPLOYEE_VIEW: ['super_admin', 'hr_manager', 'shop_owner'],

    // Customers
    CUSTOMER_CREATE: ['super_admin', 'shop_owner', 'pharmacist', 'cashier'],
    CUSTOMER_UPDATE: ['super_admin', 'shop_owner', 'pharmacist'],
    CUSTOMER_DELETE: ['super_admin', 'shop_owner'],
    CUSTOMER_VIEW: ['super_admin', 'shop_owner', 'pharmacist', 'cashier'],

    // Invoices/Sales
    INVOICE_CREATE: ['shop_owner', 'pharmacist', 'cashier'],
    INVOICE_UPDATE: ['shop_owner', 'pharmacist'],
    INVOICE_DELETE: ['shop_owner', 'pharmacist'],
    INVOICE_VIEW: ['super_admin', 'warehouse_admin', 'shop_owner', 'pharmacist', 'cashier'],

    // Purchase Requests
    PURCHASE_REQUEST_CREATE: ['shop_owner', 'pharmacist'],
    PURCHASE_REQUEST_APPROVE: ['super_admin', 'warehouse_admin'],
    PURCHASE_REQUEST_VIEW: ['super_admin', 'warehouse_admin', 'shop_owner', 'pharmacist'],

    // Dispatches
    DISPATCH_CREATE: ['super_admin', 'warehouse_admin'],
    DISPATCH_UPDATE: ['super_admin', 'warehouse_admin'],
    DISPATCH_VIEW: ['super_admin', 'warehouse_admin', 'shop_owner'],

    // Inventory
    INVENTORY_UPDATE: ['super_admin', 'warehouse_admin'],
    INVENTORY_VIEW: ['super_admin', 'warehouse_admin', 'shop_owner', 'pharmacist'],

    // Settings
    SETTINGS_UPDATE: ['super_admin'],
    SETTINGS_VIEW: ['super_admin'],

    // Reports
    REPORTS_VIEW: ['super_admin', 'warehouse_admin', 'shop_owner'],
} as const;

export type PermissionKey = keyof typeof Permissions;

/**
 * Check if user has permission for an action
 */
export const hasPermission = (userRole: string | undefined | null, permission: PermissionKey): boolean => {
    if (!userRole) return false;
    return (Permissions[permission] as readonly string[]).includes(userRole);
};

/**
 * Check if user has any of the specified roles
 */
export const hasRole = (userRole: string | undefined | null, roles: string[]): boolean => {
    if (!userRole) return false;
    return roles.includes(userRole);
};

/**
 * Get user-friendly role name
 */
export const getRoleName = (role: string): string => {
    const roleNames: Record<string, string> = {
        super_admin: 'Super Admin',
        warehouse_admin: 'Warehouse Admin',
        shop_owner: 'Shop Owner',
        pharmacist: 'Pharmacist',
        cashier: 'Cashier',
        hr_manager: 'HR Manager',
    };
    return roleNames[role] || role;
};
