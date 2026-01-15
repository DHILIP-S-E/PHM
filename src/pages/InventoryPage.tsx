import { useState, useEffect } from 'react';
import { inventoryApi } from '../services/api';
import { useOperationalContext } from '../contexts/OperationalContext';
import { WarehouseSelect } from '../components/MasterSelect';
import StatCard from '../components/StatCard';

interface StockMovement {
    id: string;
    medicine_name: string;
    batch_number: string;
    warehouse_name?: string;
    shop_name?: string;
    quantity: number;
    movement_type: 'in' | 'out' | 'transfer' | 'adjustment';
    reference_type: string;
    created_at: string;
    performed_by: string;
}

export default function InventoryPage() {
    // Operational Context for Super Admin flow
    const { activeEntity, scope } = useOperationalContext();

    const [movements, setMovements] = useState<StockMovement[]>([]);
    const [loading, setLoading] = useState(true);
    // Local filter for Super Admin in global scope
    const [selectedWarehouseId, setSelectedWarehouseId] = useState('');
    const [movementType, setMovementType] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [totalItems, setTotalItems] = useState(0);
    const pageSize = 20;

    useEffect(() => {
        fetchMovements();
    }, [currentPage, selectedWarehouseId, movementType, activeEntity]);

    const fetchMovements = async () => {
        try {
            setLoading(true);
            const params: any = { page: currentPage, size: pageSize };

            // Enforce Context
            if (activeEntity?.type === 'warehouse') {
                params.warehouse_id = activeEntity.id;
            } else if (activeEntity?.type === 'shop') {
                params.shop_id = activeEntity.id;
            } else if (scope === 'global' && selectedWarehouseId) {
                // If global, allow filtering by selected warehouse
                params.warehouse_id = selectedWarehouseId;
            }

            if (movementType) params.movement_type = movementType;

            const response = await inventoryApi.getMovements(params);

            // Extract movements array safely
            let movementsData = [];
            if (response.data) {
                if (Array.isArray(response.data)) {
                    movementsData = response.data;
                } else if (response.data.items && Array.isArray(response.data.items)) {
                    movementsData = response.data.items;
                } else if (response.data.data && Array.isArray(response.data.data)) {
                    movementsData = response.data.data;
                }
            }

            setMovements(movementsData);
            setTotalItems(response.data?.total || movementsData.length);
        } catch (err) {
            console.error('Failed to fetch movements:', err);
            setMovements([]);
            setTotalItems(0);
        } finally {
            setLoading(false);
        }
    };

    const getMovementColor = (type: string) => {
        switch (type) {
            case 'in': return 'text-green-600 bg-green-100 dark:bg-green-900/30 dark:text-green-400';
            case 'out': return 'text-red-600 bg-red-100 dark:bg-red-900/30 dark:text-red-400';
            case 'transfer': return 'text-blue-600 bg-blue-100 dark:bg-blue-900/30 dark:text-blue-400';
            case 'adjustment': return 'text-amber-600 bg-amber-100 dark:bg-amber-900/30 dark:text-amber-400';
            default: return 'text-slate-600 bg-slate-100 dark:bg-slate-700 dark:text-slate-400';
        }
    };

    const getMovementIcon = (type: string) => {
        switch (type) {
            case 'in': return 'login';
            case 'out': return 'logout';
            case 'transfer': return 'swap_horiz';
            case 'adjustment': return 'tune';
            default: return 'history';
        }
    };

    // Calculate stats
    const stats = {
        total: totalItems,
        stockIn: movements.filter(m => m.movement_type === 'in').length,
        stockOut: movements.filter(m => m.movement_type === 'out').length,
        transfers: movements.filter(m => m.movement_type === 'transfer').length
    };

    const totalPages = Math.ceil(totalItems / pageSize);

    return (
        <div className="space-y-6">
            {/* 1. PAGE HEADER */}
            <div>
                <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Inventory Movements</h1>
                <p className="text-slate-500 dark:text-slate-400 mt-1">
                    Track stock changes {scope === 'global' ? 'across all locations' : activeEntity?.name ? `for ${activeEntity.name}` : ''}
                </p>
            </div>

            {/* 2. KPI / SUMMARY STRIP */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <StatCard
                    title="Total Movements"
                    value={stats.total}
                    icon="history"
                />
                <StatCard
                    title="Stock In"
                    value={stats.stockIn}
                    icon="login"
                />
                <StatCard
                    title="Stock Out"
                    value={stats.stockOut}
                    icon="logout"
                />
                <StatCard
                    title="Transfers"
                    value={stats.transfers}
                    icon="swap_horiz"
                />
            </div>

            {/* 3. LIST CONTROLS STRIP */}
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 px-4 py-3">
                <div className="flex items-center justify-between gap-4">
                    <h2 className="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                        Movement List
                        <span className="px-2 py-0.5 text-xs font-medium bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded-full">
                            {totalItems}
                        </span>
                    </h2>
                    <div className="flex items-center gap-2">
                        {/* Warehouse Selector - ONLY visible to Super Admin in GLOBAL scope */}
                        {scope === 'global' && (
                            <select
                                value={selectedWarehouseId}
                                onChange={(e) => { setSelectedWarehouseId(e.target.value); setCurrentPage(1); }}
                                className="px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 text-slate-700 dark:text-slate-300"
                            >
                                <option value="">All Warehouses</option>
                            </select>
                        )}

                        {/* Explicit indicator of current scope if not global */}
                        {scope !== 'global' && activeEntity && (
                            <span className="px-3 py-2 text-sm rounded-lg bg-slate-100 dark:bg-slate-700 text-slate-500 flex items-center gap-1.5">
                                <span className="material-symbols-outlined text-[16px]">
                                    {activeEntity.type === 'warehouse' ? 'warehouse' : 'store'}
                                </span>
                                {activeEntity.name}
                            </span>
                        )}

                        <button className="p-2 rounded-lg border border-slate-200 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700">
                            <span className="material-symbols-outlined text-[18px] text-slate-500">filter_list</span>
                        </button>

                        <select
                            value={movementType}
                            onChange={(e) => { setMovementType(e.target.value); setCurrentPage(1); }}
                            className="px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 text-slate-700 dark:text-slate-300"
                        >
                            <option value="">All Types</option>
                            <option value="in">Stock In</option>
                            <option value="out">Stock Out</option>
                            <option value="transfer">Transfer</option>
                            <option value="adjustment">Adjustment</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* 4. ENTITY TABLE */}
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
                {loading ? (
                    <div className="flex items-center justify-center py-16">
                        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
                    </div>
                ) : movements.length === 0 ? (
                    <div className="py-16 text-center">
                        <span className="material-symbols-outlined text-5xl text-slate-300 dark:text-slate-600 mb-3">history_toggle_off</span>
                        <h3 className="text-lg font-medium text-slate-900 dark:text-white">No movements found</h3>
                        <p className="text-slate-500 dark:text-slate-400 mt-1">Adjust filters to see stock history</p>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-slate-50 dark:bg-slate-900/50">
                                <tr>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Details</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Product</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Type</th>
                                    <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Qty</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Location</th>
                                    <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Date</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                                {movements.map((move, index) => (
                                    <tr key={move.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                                        <td className="px-4 py-2.5">
                                            <div className="flex flex-col">
                                                <span className="text-[11px] font-mono text-slate-500">{move.reference_type.toUpperCase()}</span>
                                                <span className="text-[11px] text-slate-400">By: {move.performed_by || 'System'}</span>
                                            </div>
                                        </td>
                                        <td className="px-4 py-2.5">
                                            <div>
                                                <p className="font-medium text-sm text-slate-900 dark:text-white">{move.medicine_name}</p>
                                                <p className="text-[11px] text-slate-500">Batch: {move.batch_number}</p>
                                            </div>
                                        </td>
                                        <td className="px-4 py-2.5">
                                            <span className={`inline-flex items-center gap-0.5 px-2 py-0.5 rounded-full text-[11px] font-medium ${getMovementColor(move.movement_type)}`}>
                                                <span className="material-symbols-outlined text-[12px]">{getMovementIcon(move.movement_type)}</span>
                                                <span className="capitalize">{move.movement_type}</span>
                                            </span>
                                        </td>
                                        <td className="px-4 py-2.5 text-right">
                                            <span className={`font-mono text-sm font-medium ${move.movement_type === 'out' ? 'text-red-600' : 'text-green-600'}`}>
                                                {move.movement_type === 'out' ? '-' : '+'}{Math.abs(move.quantity)}
                                            </span>
                                        </td>
                                        <td className="px-4 py-2.5 text-xs text-slate-600 dark:text-slate-400">
                                            {move.warehouse_name || move.shop_name || '-'}
                                        </td>
                                        <td className="px-4 py-2.5 text-right text-xs text-slate-500 dark:text-slate-400">
                                            {new Date(move.created_at).toLocaleDateString()}
                                            <div className="text-[10px]">{new Date(move.created_at).toLocaleTimeString()}</div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                {/* Pagination */}
                {totalPages > 1 && (
                    <div className="px-6 py-4 border-t border-slate-200 dark:border-slate-700 flex items-center justify-between">
                        <p className="text-sm text-slate-500">
                            Showing {(currentPage - 1) * pageSize + 1} to {Math.min(currentPage * pageSize, totalItems)} of {totalItems}
                        </p>
                        <div className="flex items-center gap-2">
                            <button
                                onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                                disabled={currentPage === 1}
                                className="p-2 rounded-lg border border-slate-200 dark:border-slate-600 disabled:opacity-50"
                            >
                                <span className="material-symbols-outlined text-[20px]">chevron_left</span>
                            </button>
                            <span className="px-4 py-2 text-sm font-medium">Page {currentPage} of {totalPages}</span>
                            <button
                                onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                                disabled={currentPage === totalPages}
                                className="p-2 rounded-lg border border-slate-200 dark:border-slate-600 disabled:opacity-50"
                            >
                                <span className="material-symbols-outlined text-[20px]">chevron_right</span>
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
