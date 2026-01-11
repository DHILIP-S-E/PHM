import type { ReactNode } from 'react';
import { usePermissions } from '../contexts/PermissionContext';

interface PermissionGateProps {
    /**
     * Single permission to check
     */
    permission?: string;
    /**
     * Check if user has ANY of these permissions
     */
    anyOf?: string[];
    /**
     * Check if user has ALL of these permissions
     */
    allOf?: string[];
    /**
     * Check if user has access to a module (any permission starting with module.)
     */
    module?: string;
    /**
     * Content to render if permission check passes
     */
    children: ReactNode;
    /**
     * Optional fallback content to render if permission check fails
     */
    fallback?: ReactNode;
}

/**
 * Component that conditionally renders children based on user permissions.
 * 
 * Usage:
 * ```tsx
 * <PermissionGate permission="users.create">
 *   <CreateUserButton />
 * </PermissionGate>
 * 
 * <PermissionGate anyOf={["inventory.view.global", "inventory.view.warehouse"]}>
 *   <InventoryPage />
 * </PermissionGate>
 * ```
 */
export function PermissionGate({
    permission,
    anyOf,
    allOf,
    module,
    children,
    fallback = null
}: PermissionGateProps) {
    const { hasPermission, hasAnyPermission, hasAllPermissions, hasModuleAccess } = usePermissions();

    let isAllowed = false;

    if (permission) {
        isAllowed = hasPermission(permission);
    } else if (anyOf && anyOf.length > 0) {
        isAllowed = hasAnyPermission(anyOf);
    } else if (allOf && allOf.length > 0) {
        isAllowed = hasAllPermissions(allOf);
    } else if (module) {
        isAllowed = hasModuleAccess(module);
    } else {
        // No permission specified, allow by default
        isAllowed = true;
    }

    return isAllowed ? <>{children}</> : <>{fallback}</>;
}

export default PermissionGate;
