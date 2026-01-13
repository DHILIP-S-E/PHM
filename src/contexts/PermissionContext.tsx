import { createContext, useContext, type ReactNode } from 'react';
import { useUser } from './UserContext';
import { hasPermission, hasAnyPermission, hasAllPermissions, hasModuleAccess, getScopeForPermission } from '../types/permissions';

interface PermissionContextType {
    permissions: string[];
    hasPermission: (permission: string) => boolean;
    hasAnyPermission: (permissions: string[]) => boolean;
    hasAllPermissions: (permissions: string[]) => boolean;
    hasModuleAccess: (module: string) => boolean;
    getScopeForPermission: (permissionPrefix: string) => string | null;
}

const PermissionContext = createContext<PermissionContextType | undefined>(undefined);

export function PermissionProvider({ children }: { children: ReactNode }) {
    const { user } = useUser();
    const permissions = user?.permissions ?? [];
    const isSuperAdmin = user?.role === 'super_admin';

    const value: PermissionContextType = {
        permissions,
        hasPermission: (permission: string) => {
            // Super Admin bypasses all permission checks
            if (isSuperAdmin) return true;
            return hasPermission(permissions, permission);
        },
        hasAnyPermission: (perms: string[]) => {
            // Super Admin bypasses all permission checks
            if (isSuperAdmin) return true;
            return hasAnyPermission(permissions, perms);
        },
        hasAllPermissions: (perms: string[]) => {
            // Super Admin bypasses all permission checks
            if (isSuperAdmin) return true;
            return hasAllPermissions(permissions, perms);
        },
        hasModuleAccess: (module: string) => {
            // Super Admin bypasses all permission checks
            if (isSuperAdmin) return true;
            return hasModuleAccess(permissions, module);
        },
        getScopeForPermission: (prefix: string) => {
            // Super Admin always has global scope
            if (isSuperAdmin) return 'global';
            return getScopeForPermission(permissions, prefix);
        },
    };

    return (
        <PermissionContext.Provider value={value}>
            {children}
        </PermissionContext.Provider>
    );
}

/**
 * Hook to access permission checking functions
 */
export function usePermissions(): PermissionContextType {
    const context = useContext(PermissionContext);
    if (context === undefined) {
        throw new Error('usePermissions must be used within a PermissionProvider');
    }
    return context;
}

/**
 * Hook to check a single permission
 */
export function useHasPermission(permission: string): boolean {
    const { hasPermission } = usePermissions();
    return hasPermission(permission);
}

/**
 * Hook to check if user has any of the listed permissions
 */
export function useHasAnyPermission(permissions: string[]): boolean {
    const { hasAnyPermission } = usePermissions();
    return hasAnyPermission(permissions);
}

export default PermissionContext;
