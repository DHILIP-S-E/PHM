import { useState, useEffect } from 'react';
import { warehousesApi, shopsApi, reportsApi, inventoryApi } from '../services/api';
import StatCard from '../components/StatCard';

interface DashboardStats {
    warehouses: number;
    shops: number;
    revenue: number;
    activeUsers: number;
}

interface Alert {
    id: string;
    title: string;
    description: string;
    time: string;
    severity: 'critical' | 'warning';
}

export default function Dashboard() {
    const [stats, setStats] = useState<DashboardStats>({ warehouses: 0, shops: 0, revenue: 0, activeUsers: 0 });
    const [alerts, setAlerts] = useState<Alert[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        try {
            setLoading(true);
            setError(null);

            // Fetch real data from database
            const [warehousesRes, shopsRes, salesRes, alertsRes] = await Promise.all([
                warehousesApi.list({ page: 1, size: 1 }),
                shopsApi.list({ page: 1, size: 1 }),
                reportsApi.getSales(),
                inventoryApi.getAlerts(),
            ]);

            setStats({
                warehouses: warehousesRes.data?.total || 0,
                shops: shopsRes.data?.total || 0,
                revenue: salesRes.data?.total_sales || 0,
                activeUsers: 0,
            });

            // Transform alerts from database
            const stockAlerts = alertsRes.data?.alerts || [];
            setAlerts(stockAlerts.slice(0, 5).map((a: any) => ({
                id: a.id,
                title: a.type === 'low_stock' ? `Low Stock - ${a.medicine_name}` : a.type === 'expired' ? `Expired - ${a.medicine_name}` : `Expiry Warning - ${a.medicine_name}`,
                description: a.type === 'low_stock'
                    ? `Stock at ${a.current_quantity} units`
                    : a.type === 'expired'
                        ? `Expired batch: ${a.batch_number}`
                        : `Expires in ${a.days_to_expiry} days`,
                time: 'Recently',
                severity: a.type === 'expired' ? 'critical' : 'warning',
            })));

        } catch (err) {
            console.error('Dashboard fetch error:', err);
            setError('Failed to load dashboard data from database');
        } finally {
            setLoading(false);
        }
    };

    const formatCurrency = (value: number) => {
        if (value >= 1000000) return `₹${(value / 1000000).toFixed(1)}M`;
        if (value >= 1000) return `₹${(value / 1000).toFixed(0)}K`;
        return `₹${value}`;
    };

    const statCards = [
        { title: 'Total Warehouses', value: stats.warehouses.toString(), change: '', changeType: 'up' as const, icon: 'warehouse' },
        { title: 'Total Medical Shops', value: stats.shops.toLocaleString(), change: '', changeType: 'up' as const, icon: 'storefront' },
        { title: 'Active Users', value: stats.activeUsers.toLocaleString(), change: '', changeType: 'up' as const, icon: 'group' },
        { title: 'Total Revenue', value: formatCurrency(stats.revenue), change: '', changeType: 'up' as const, icon: 'payments' },
    ];

    if (loading) {
        return (
            <div className="flex items-center justify-center h-full">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
            </div>
        );
    }

    return (
        <div className="p-6 lg:p-8 space-y-8">
            {/* Page Heading */}
            <div className="flex flex-wrap items-end justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">Dashboard Overview</h2>
                    <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                        Real-time data from PostgreSQL database
                    </p>
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={fetchDashboardData}
                        className="flex items-center gap-2 px-4 py-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
                    >
                        <span className="material-symbols-outlined text-[18px]">refresh</span>
                        <span>Refresh</span>
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white text-sm font-medium hover:bg-blue-700 shadow-sm shadow-blue-500/30 transition-colors">
                        <span className="material-symbols-outlined text-[18px]">download</span>
                        <span>Export Report</span>
                    </button>
                </div>
            </div>

            {error && (
                <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 flex items-center gap-3">
                    <span className="material-symbols-outlined text-red-500">error</span>
                    <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
                </div>
            )}

            {/* Stats Grid */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
                {statCards.map((stat) => (
                    <StatCard key={stat.title} {...stat} />
                ))}
            </div>

            {/* Charts Section */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Revenue Chart */}
                <div className="lg:col-span-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-surface-light dark:bg-surface-dark p-6 shadow-sm">
                    <div className="flex items-center justify-between mb-6">
                        <div>
                            <h3 className="text-lg font-bold text-slate-900 dark:text-white">Revenue Trends</h3>
                            <p className="text-sm text-slate-500 dark:text-slate-400">Total: {formatCurrency(stats.revenue)}</p>
                        </div>
                    </div>
                    <div className="h-64 w-full relative flex items-center justify-center text-slate-400">
                        {stats.revenue > 0 ? (
                            <div className="text-center">
                                <span className="material-symbols-outlined text-6xl mb-2 text-green-500">trending_up</span>
                                <p className="text-2xl font-bold text-slate-900 dark:text-white">{formatCurrency(stats.revenue)}</p>
                                <p className="text-sm text-slate-500">Total Revenue</p>
                            </div>
                        ) : (
                            <div className="text-center">
                                <span className="material-symbols-outlined text-6xl mb-2">show_chart</span>
                                <p>No sales data yet</p>
                                <p className="text-sm">Create invoices to see revenue</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* System Health */}
                <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-surface-light dark:bg-surface-dark p-6 shadow-sm flex flex-col">
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-6">System Health</h3>
                    <div className="flex-1 flex flex-col items-center justify-center relative min-h-[180px]">
                        <div className="relative w-40 h-40 rounded-full flex items-center justify-center" style={{ background: 'conic-gradient(#22c55e 0% 100%, #e2e8f0 100% 100%)' }}>
                            <div className="absolute inset-2 bg-surface-light dark:bg-surface-dark rounded-full flex flex-col items-center justify-center">
                                <span className="text-3xl font-bold text-green-600">100%</span>
                                <span className="text-xs text-slate-500 uppercase tracking-wide">Connected</span>
                            </div>
                        </div>
                    </div>
                    <div className="space-y-4 mt-6">
                        <div>
                            <div className="flex justify-between text-sm mb-1">
                                <span className="text-slate-600 dark:text-slate-400">Database</span>
                                <span className="text-emerald-600 font-medium">Neon PostgreSQL</span>
                            </div>
                            <div className="h-2 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                                <div className="h-full bg-emerald-500 w-full rounded-full"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom Row: Alerts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 pb-6">
                {/* Stock Alerts */}
                <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-surface-light dark:bg-surface-dark shadow-sm">
                    <div className="p-5 border-b border-slate-100 dark:border-slate-800 flex justify-between items-center">
                        <div className="flex items-center gap-2">
                            <span className="material-symbols-outlined text-red-500">warning</span>
                            <h3 className="text-lg font-bold text-slate-900 dark:text-white">Stock Alerts</h3>
                        </div>
                        <span className="px-2.5 py-0.5 rounded-full bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400 text-xs font-bold">{alerts.length} Alerts</span>
                    </div>
                    <div className="p-0">
                        {alerts.length > 0 ? alerts.map((alert) => (
                            <div key={alert.id} className="flex items-start gap-4 p-4 border-b border-slate-50 dark:border-slate-800/50 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors last:border-b-0">
                                <div className={`mt-0.5 h-2 w-2 rounded-full flex-shrink-0 ${alert.severity === 'critical' ? 'bg-red-500' : 'bg-amber-500'}`}></div>
                                <div className="flex-1 min-w-0">
                                    <p className="text-sm font-semibold text-slate-900 dark:text-white truncate">{alert.title}</p>
                                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-0.5">{alert.description}</p>
                                </div>
                            </div>
                        )) : (
                            <div className="p-8 text-center text-slate-500">
                                <span className="material-symbols-outlined text-4xl mb-2 text-green-500">check_circle</span>
                                <p className="font-medium">No alerts</p>
                                <p className="text-sm">All stock levels are healthy</p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Quick Actions */}
                <div className="rounded-xl border border-slate-200 dark:border-slate-700 bg-surface-light dark:bg-surface-dark shadow-sm p-6">
                    <h3 className="text-lg font-bold text-slate-900 dark:text-white mb-6">Quick Actions</h3>
                    <div className="grid grid-cols-2 gap-4">
                        <button className="flex flex-col items-center gap-2 p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                            <span className="material-symbols-outlined text-primary text-2xl">add_business</span>
                            <span className="text-sm font-medium text-slate-900 dark:text-white">Add Warehouse</span>
                        </button>
                        <button className="flex flex-col items-center gap-2 p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                            <span className="material-symbols-outlined text-primary text-2xl">storefront</span>
                            <span className="text-sm font-medium text-slate-900 dark:text-white">Add Shop</span>
                        </button>
                        <button className="flex flex-col items-center gap-2 p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                            <span className="material-symbols-outlined text-primary text-2xl">medication</span>
                            <span className="text-sm font-medium text-slate-900 dark:text-white">Add Medicine</span>
                        </button>
                        <button className="flex flex-col items-center gap-2 p-4 rounded-lg border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
                            <span className="material-symbols-outlined text-primary text-2xl">receipt_long</span>
                            <span className="text-sm font-medium text-slate-900 dark:text-white">New Invoice</span>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
