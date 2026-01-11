/**
 * Role-Based Access Control Utilities (LEGACY COMPATIBILITY LAYER)
 * 
 * NOTE: This file is maintained for backward compatibility.
 * New code should use usePermissions() hook from PermissionContext.
 * 
 * @deprecated Use usePermissions(), useHasPermission(), or PermissionGate instead.
 */

/**
 * @deprecated Use usePermissions().hasAnyPermission() instead
 * Check if user has permission (legacy role-based check)
 */
export const hasPermission = (userRole: string | undefined | null, _permissionKey: string): boolean => {
    console.warn('hasPermission from rbac.ts is deprecated. Use usePermissions() hook instead.');
    if (!userRole) return false;
    // Super admin has all permissions
    if (userRole === 'super_admin') return true;
    return false; // For other roles, use the new permission system
};

/**
 * @deprecated Use new permission-based checks
 * Check if user has any of the specified roles
 */
export const hasRole = (userRole: string | undefined | null, roles: string[]): boolean => {
    if (!userRole) return false;
    return roles.includes(userRole);
};

/**
 * Get user-friendly role name
 * This is still useful for display purposes
 */
export const getRoleName = (role: string): string => {
    // Convert role code to readable name
    // e.g., "warehouse_admin" -> "Warehouse Admin"
    return role
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
};

/**
 * Get role badge color for UI
 */
export const getRoleBadgeColor = (role: string): string => {
    const roleColors: Record<string, string> = {
        super_admin: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300',
        warehouse_admin: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
        warehouse_employee: 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-300',
        pharmacy_admin: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300',
        pharmacy_employee: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300',
        shop_owner: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300',
        pharmacist: 'bg-teal-100 text-teal-700 dark:bg-teal-900/30 dark:text-teal-300',
        cashier: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300',
    };
    return roleColors[role] || 'bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300';
};
