/**
 * useMasterOptions Hook - Fetches configurable options from the database
 * 
 * Use this hook to replace hardcoded dropdown options with database-driven values.
 * 
 * Categories available:
 * - entity_status: Active, Inactive, Maintenance, Suspended
 * - shop_type: Retail, Wholesale, Franchise, Hospital, Clinic
 * - priority: Low, Normal, High, Urgent
 * - request_status: Pending, Approved, Partial, Rejected, Completed, Dispatched
 * - dispatch_status: Created, Packed, Dispatched, In Transit, Delivered, Cancelled
 * - invoice_status: Draft, Completed, Cancelled, Returned
 * - payment_status: Pending, Partial, Completed, Refunded
 * - attendance_status: Present, Absent, Half Day, Leave
 * - medicine_type: Tablet, Capsule, Syrup, Injection, etc.
 * - notification_type: Info, Success, Warning, Error, Stock, Expiry
 * 
 * Usage:
 * const { options, loading, error } = useMasterOptions('shop_type');
 */

import { useState, useEffect, useCallback } from 'react';
import { masterOptionsApi } from '../services/api';

export interface MasterOption {
    id: string;
    category: string;
    code: string;
    label: string;
    description: string | null;
    display_order: number;
    is_active: boolean;
    is_system: boolean;
    color: string | null;
    icon: string | null;
}

interface UseMasterOptionsResult {
    options: MasterOption[];
    loading: boolean;
    error: string | null;
    refresh: () => Promise<void>;
}

// Cache to avoid refetching the same category
const optionsCache: Record<string, { options: MasterOption[]; timestamp: number }> = {};
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

export function useMasterOptions(category: string, includeInactive: boolean = false): UseMasterOptionsResult {
    const [options, setOptions] = useState<MasterOption[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchOptions = useCallback(async () => {
        // Check cache first
        const cacheKey = `${category}_${includeInactive}`;
        const cached = optionsCache[cacheKey];

        if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
            setOptions(cached.options);
            setLoading(false);
            return;
        }

        try {
            setLoading(true);
            setError(null);
            const response = await masterOptionsApi.getByCategory(category, includeInactive);
            const data = response.data || [];

            // Update cache
            optionsCache[cacheKey] = { options: data, timestamp: Date.now() };

            setOptions(data);
        } catch (err: any) {
            console.error(`Failed to fetch master options for ${category}:`, err);
            setError(err.message || 'Failed to load options');
            setOptions([]);
        } finally {
            setLoading(false);
        }
    }, [category, includeInactive]);

    useEffect(() => {
        fetchOptions();
    }, [fetchOptions]);

    const refresh = useCallback(async () => {
        // Clear cache for this category
        const cacheKey = `${category}_${includeInactive}`;
        delete optionsCache[cacheKey];
        await fetchOptions();
    }, [category, includeInactive, fetchOptions]);

    return { options, loading, error, refresh };
}

/**
 * Helper to get color class from option color
 */
export function getOptionColorClass(color: string | null): string {
    const colorMap: Record<string, string> = {
        green: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300',
        red: 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300',
        amber: 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300',
        blue: 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300',
        purple: 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300',
        cyan: 'bg-cyan-100 text-cyan-700 dark:bg-cyan-900/30 dark:text-cyan-300',
        teal: 'bg-teal-100 text-teal-700 dark:bg-teal-900/30 dark:text-teal-300',
        slate: 'bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300',
        orange: 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300',
        emerald: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300',
    };
    return colorMap[color || 'slate'] || colorMap.slate;
}

/**
 * Clear entire options cache (call after creating/updating options)
 */
export function clearOptionsCache(): void {
    Object.keys(optionsCache).forEach(key => delete optionsCache[key]);
}

export default useMasterOptions;
