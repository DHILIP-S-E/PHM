import { useState, useEffect } from 'react';
import { dispatchesApi } from '../services/api';

interface Dispatch {
    id: string;
    dispatch_number: string;
    warehouse_name: string;
    shop_name: string;
    status: string;
    total_items: number;
    dispatch_date: string;
    received_date?: string;
    expected_date?: string;
    driver_name?: string;
    vehicle_number?: string;
}

export default function DispatchesList() {
    const [dispatches, setDispatches] = useState<Dispatch[]>([]);
    const [loading, setLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState('');
    const [selectedDispatch, setSelectedDispatch] = useState<Dispatch | null>(null);
    const [updating, setUpdating] = useState(false);

    useEffect(() => { fetchDispatches(); }, [statusFilter]);

    const fetchDispatches = async () => {
        try {
            setLoading(true);
            const res = await dispatchesApi.list({ status: statusFilter || undefined });
            setDispatches(res.data?.items || res.data || []);
        } catch (e) { console.error(e); }
        finally { setLoading(false); }
    };

    const handleUpdateStatus = async (id: string, newStatus: string) => {
        try {
            setUpdating(true);
            await dispatchesApi.updateStatus(id, newStatus);
            fetchDispatches();
            setSelectedDispatch(null);
        } catch (e) {
            console.error(e);
            alert('Failed to update status');
        } finally { setUpdating(false); }
    };

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'delivered': return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400';
            case 'in_transit': return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400';
            case 'pending': return 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400';
            case 'cancelled': return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400';
            default: return 'bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-300';
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'delivered': return 'check_circle';
            case 'in_transit': return 'local_shipping';
            case 'pending': return 'schedule';
            case 'cancelled': return 'cancel';
            default: return 'help';
        }
    };

    const stats = {
        total: dispatches.length,
        pending: dispatches.filter(d => d.status === 'pending').length,
        inTransit: dispatches.filter(d => d.status === 'in_transit').length,
        delivered: dispatches.filter(d => d.status === 'delivered').length,
    };

    return (
        <div className="space-y-6">
            {/* Header */}
            <div className="flex flex-wrap items-end justify-between gap-4 animate-fadeIn">
                <div>
                    <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white tracking-tight">Dispatch History</h1>
                    <p className="text-slate-500 dark:text-slate-400 mt-1">Track warehouse to shop deliveries and monitor shipment status</p>
                </div>
                <div className="flex items-center gap-3">
                    <button onClick={fetchDispatches} className="flex items-center gap-2 px-4 py-2.5 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors shadow-sm">
                        <span className="material-symbols-outlined text-[20px]">refresh</span>
                        <span className="hidden sm:inline">Refresh</span>
                    </button>
                    <button className="flex items-center gap-2 px-4 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all shadow-lg shadow-blue-500/30 hover:-translate-y-0.5 font-medium">
                        <span className="material-symbols-outlined text-[20px]">download</span>
                        Export
                    </button>
                </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm relative overflow-hidden animate-fadeInUp" style={{ animationDelay: '50ms' }}>
                    <div className="absolute right-0 top-0 h-full w-1 bg-slate-400"></div>
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Total Dispatches</p>
                            <p className="text-2xl font-bold text-slate-900 dark:text-white mt-1">{stats.total}</p>
                        </div>
                        <div className="w-12 h-12 rounded-lg bg-slate-100 dark:bg-slate-700 flex items-center justify-center">
                            <span className="material-symbols-outlined text-slate-600 dark:text-slate-400">inventory_2</span>
                        </div>
                    </div>
                </div>
                <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm relative overflow-hidden animate-fadeInUp" style={{ animationDelay: '100ms' }}>
                    <div className="absolute right-0 top-0 h-full w-1 bg-amber-500"></div>
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Pending</p>
                            <p className="text-2xl font-bold text-amber-600 mt-1">{stats.pending}</p>
                        </div>
                        <div className="w-12 h-12 rounded-lg bg-amber-100 dark:bg-amber-900/30 flex items-center justify-center">
                            <span className="material-symbols-outlined text-amber-600 dark:text-amber-400">schedule</span>
                        </div>
                    </div>
                </div>
                <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm relative overflow-hidden animate-fadeInUp" style={{ animationDelay: '150ms' }}>
                    <div className="absolute right-0 top-0 h-full w-1 bg-blue-500"></div>
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-slate-500 dark:text-slate-400">In Transit</p>
                            <p className="text-2xl font-bold text-blue-600 mt-1">{stats.inTransit}</p>
                        </div>
                        <div className="w-12 h-12 rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                            <span className="material-symbols-outlined text-blue-600 dark:text-blue-400">local_shipping</span>
                        </div>
                    </div>
                </div>
                <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-5 shadow-sm relative overflow-hidden animate-fadeInUp" style={{ animationDelay: '200ms' }}>
                    <div className="absolute right-0 top-0 h-full w-1 bg-green-500"></div>
                    <div className="flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-slate-500 dark:text-slate-400">Delivered</p>
                            <p className="text-2xl font-bold text-green-600 mt-1">{stats.delivered}</p>
                        </div>
                        <div className="w-12 h-12 rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center">
                            <span className="material-symbols-outlined text-green-600 dark:text-green-400">check_circle</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Filters Toolbar */}
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 p-4 shadow-sm animate-fadeIn">
                <div className="flex flex-wrap items-center gap-4">
                    <div className="relative flex-1 max-w-md">
                        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                            <span className="material-symbols-outlined text-[20px]">search</span>
                        </span>
                        <input
                            type="text"
                            placeholder="Search by dispatch ID or destination..."
                            className="w-full pl-10 pr-4 py-2.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
                        />
                    </div>
                    <div className="relative">
                        <select
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                            className="appearance-none pl-4 pr-10 py-2.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm focus:ring-2 focus:ring-blue-500 cursor-pointer"
                        >
                            <option value="">All Status</option>
                            <option value="pending">Pending</option>
                            <option value="in_transit">In Transit</option>
                            <option value="delivered">Delivered</option>
                            <option value="cancelled">Cancelled</option>
                        </select>
                        <span className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none">
                            <span className="material-symbols-outlined text-[18px]">expand_more</span>
                        </span>
                    </div>
                    <button className="flex items-center gap-2 px-4 py-2.5 text-sm font-medium text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-700 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-600 transition-colors">
                        <span className="material-symbols-outlined text-[18px]">calendar_today</span>
                        Date Range
                    </button>
                </div>
            </div>

            {/* Table */}
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
                {loading ? (
                    <div className="flex justify-center h-64 items-center">
                        <div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full"></div>
                    </div>
                ) : dispatches.length === 0 ? (
                    <div className="flex flex-col items-center justify-center py-16 text-slate-500">
                        <span className="material-symbols-outlined text-5xl mb-3">local_shipping</span>
                        <p className="font-medium text-lg">No dispatches yet</p>
                        <p className="text-sm">Dispatches will appear when purchase requests are approved</p>
                    </div>
                ) : (
                    <table className="w-full">
                        <thead className="bg-slate-50 dark:bg-slate-900/50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Dispatch #</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">From Warehouse</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">To Shop</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Items</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Date</th>
                                <th className="px-6 py-3 text-right text-xs font-semibold text-slate-500 uppercase">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                            {dispatches.map((d, index) => (
                                <tr key={d.id} className="hover:bg-slate-50 dark:hover:bg-slate-900/30 transition-colors group animate-fadeIn" style={{ animationDelay: `${index * 30}ms` }}>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-2">
                                            <span className={`material-symbols-outlined text-[18px] ${d.status === 'delivered' ? 'text-green-500' : d.status === 'in_transit' ? 'text-blue-500' : 'text-amber-500'}`}>
                                                {getStatusIcon(d.status)}
                                            </span>
                                            <span className="font-mono text-sm text-slate-900 dark:text-white">{d.dispatch_number || d.id.slice(0, 8)}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4 text-slate-700 dark:text-slate-300">{d.warehouse_name || 'N/A'}</td>
                                    <td className="px-6 py-4 text-slate-700 dark:text-slate-300">{d.shop_name || 'N/A'}</td>
                                    <td className="px-6 py-4 text-slate-500">{d.total_items || 0} items</td>
                                    <td className="px-6 py-4">
                                        <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${getStatusColor(d.status)}`}>
                                            {d.status.replace('_', ' ')}
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 text-sm text-slate-500">{new Date(d.dispatch_date).toLocaleDateString()}</td>
                                    <td className="px-6 py-4 text-right">
                                        <div className="flex gap-2 justify-end">
                                            <button
                                                onClick={() => setSelectedDispatch(d)}
                                                className="p-2 text-slate-400 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-all" title="View Details"
                                            >
                                                <span className="material-symbols-outlined text-[20px]">visibility</span>
                                            </button>
                                            {d.status === 'pending' && (
                                                <button
                                                    onClick={() => handleUpdateStatus(d.id, 'in_transit')}
                                                    className="px-3 py-1.5 text-xs font-medium bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                                                    disabled={updating}
                                                >
                                                    Start
                                                </button>
                                            )}
                                            {d.status === 'in_transit' && (
                                                <button
                                                    onClick={() => handleUpdateStatus(d.id, 'delivered')}
                                                    className="px-3 py-1.5 text-xs font-medium bg-green-600 text-white rounded-lg hover:bg-green-700"
                                                    disabled={updating}
                                                >
                                                    Delivered
                                                </button>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>

            {/* Dispatch Detail Modal */}
            {selectedDispatch && (
                <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fadeIn">
                    <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl w-full max-w-lg border border-slate-200 dark:border-slate-700 animate-scaleIn">
                        <div className="p-6 border-b border-slate-200 dark:border-slate-700">
                            <div className="flex justify-between items-start">
                                <div>
                                    <h2 className="text-xl font-bold text-slate-900 dark:text-white">Dispatch Details</h2>
                                    <p className="text-sm text-slate-500 font-mono">{selectedDispatch.dispatch_number || selectedDispatch.id.slice(0, 8)}</p>
                                </div>
                                <button onClick={() => setSelectedDispatch(null)} className="text-slate-400 hover:text-slate-600">
                                    <span className="material-symbols-outlined">close</span>
                                </button>
                            </div>
                        </div>
                        <div className="p-6 space-y-4">
                            {/* Tracking Timeline */}
                            <div className="space-y-3">
                                <h3 className="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase">Tracking</h3>
                                <div className="flex items-center gap-4">
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${selectedDispatch.status !== 'cancelled' ? 'bg-green-100 text-green-600' : 'bg-slate-100 text-slate-400'}`}>
                                        <span className="material-symbols-outlined text-[18px]">check</span>
                                    </div>
                                    <div className={`flex-1 h-1 ${selectedDispatch.status === 'in_transit' || selectedDispatch.status === 'delivered' ? 'bg-blue-500' : 'bg-slate-200'}`}></div>
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${selectedDispatch.status === 'in_transit' || selectedDispatch.status === 'delivered' ? 'bg-blue-100 text-blue-600' : 'bg-slate-100 text-slate-400'}`}>
                                        <span className="material-symbols-outlined text-[18px]">local_shipping</span>
                                    </div>
                                    <div className={`flex-1 h-1 ${selectedDispatch.status === 'delivered' ? 'bg-green-500' : 'bg-slate-200'}`}></div>
                                    <div className={`w-8 h-8 rounded-full flex items-center justify-center ${selectedDispatch.status === 'delivered' ? 'bg-green-100 text-green-600' : 'bg-slate-100 text-slate-400'}`}>
                                        <span className="material-symbols-outlined text-[18px]">where_to_vote</span>
                                    </div>
                                </div>
                                <div className="flex justify-between text-xs text-slate-500">
                                    <span>Dispatched</span>
                                    <span>In Transit</span>
                                    <span>Delivered</span>
                                </div>
                            </div>

                            {/* Details */}
                            <div className="grid grid-cols-2 gap-4 pt-4 border-t border-slate-200 dark:border-slate-700">
                                <div>
                                    <p className="text-xs text-slate-500">From Warehouse</p>
                                    <p className="font-medium text-slate-900 dark:text-white">{selectedDispatch.warehouse_name || 'N/A'}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-slate-500">To Shop</p>
                                    <p className="font-medium text-slate-900 dark:text-white">{selectedDispatch.shop_name || 'N/A'}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-slate-500">Dispatch Date</p>
                                    <p className="font-medium text-slate-900 dark:text-white">{new Date(selectedDispatch.dispatch_date).toLocaleDateString()}</p>
                                </div>
                                <div>
                                    <p className="text-xs text-slate-500">Total Items</p>
                                    <p className="font-medium text-slate-900 dark:text-white">{selectedDispatch.total_items || 0}</p>
                                </div>
                            </div>

                            {/* Actions */}
                            <div className="flex gap-3 pt-4 border-t border-slate-200 dark:border-slate-700">
                                {selectedDispatch.status === 'pending' && (
                                    <button
                                        onClick={() => handleUpdateStatus(selectedDispatch.id, 'in_transit')}
                                        className="flex-1 py-2.5 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
                                        disabled={updating}
                                    >
                                        {updating ? 'Updating...' : '🚚 Start Dispatch'}
                                    </button>
                                )}
                                {selectedDispatch.status === 'in_transit' && (
                                    <button
                                        onClick={() => handleUpdateStatus(selectedDispatch.id, 'delivered')}
                                        className="flex-1 py-2.5 bg-green-600 text-white rounded-lg font-medium hover:bg-green-700"
                                        disabled={updating}
                                    >
                                        {updating ? 'Updating...' : '✓ Mark Delivered'}
                                    </button>
                                )}
                                {selectedDispatch.status === 'delivered' && (
                                    <div className="flex-1 py-2.5 bg-green-100 text-green-700 rounded-lg font-medium text-center">
                                        ✓ Delivered Successfully
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

