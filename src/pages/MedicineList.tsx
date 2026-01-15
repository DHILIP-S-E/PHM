import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { medicinesApi } from '../services/api';
import { useUser } from '../contexts/UserContext';
import { CategorySelect } from '../components/MasterSelect';
import StatCard from '../components/StatCard';
import SearchBar from '../components/SearchBar';

interface Medicine {
    id: string;
    name: string;
    generic_name: string;
    brand?: string;
    manufacturer: string;
    medicine_type: string;
    category?: string;
    composition?: string;
    strength?: string;
    unit?: string;
    pack_size?: number;
    hsn_code?: string;
    gst_rate?: number;
    mrp: number;
    purchase_price: number;
    total_stock: number;
    is_active: boolean;
    rack_number?: string;
    rack_name?: string;
}

export default function MedicineList() {
    const navigate = useNavigate();
    const { user } = useUser();
    const userRole = user?.role || 'user';
    const canDelete = userRole === 'super_admin';

    const [medicines, setMedicines] = useState<Medicine[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [categoryFilter, setCategoryFilter] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [totalItems, setTotalItems] = useState(0);
    const pageSize = 15;

    useEffect(() => {
        fetchMedicines();
    }, [currentPage, search, categoryFilter]);

    const fetchMedicines = async () => {
        try {
            setLoading(true);
            const params: any = { page: currentPage, size: pageSize };
            if (search) params.search = search;
            if (categoryFilter) params.category = categoryFilter;

            const response = await medicinesApi.list(params);
            setMedicines(response.data.items || []);
            setTotalItems(response.data.total || 0);
        } catch (err) {
            console.error('Failed to fetch medicines:', err);
            setMedicines([]);
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (medicine: Medicine) => {
        if (!confirm(`Are you sure you want to delete "${medicine.name}"?`)) return;

        try {
            await medicinesApi.delete(medicine.id);
            fetchMedicines();
        } catch (err: any) {
            console.error('Failed to delete medicine:', err);
            alert(err.response?.data?.detail || 'Failed to delete medicine');
        }
    };

    // Calculate stats
    const stats = {
        total: totalItems,
        active: medicines.filter(m => m.is_active).length,
        lowStock: medicines.filter(m => m.total_stock < 50).length,
        categories: new Set(medicines.map(m => m.category).filter(Boolean)).size
    };

    const totalPages = Math.ceil(totalItems / pageSize);

    return (
        <div className="space-y-6">
            {/* 1. PAGE HEADER */}
            <div className="flex justify-between items-start">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Medicines</h1>
                    <p className="text-slate-500 dark:text-slate-400 mt-1">Manage your medicine catalog</p>
                </div>
                <button
                    onClick={() => navigate('/medicines/add')}
                    className="flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 shadow-lg shadow-blue-500/30 transition-all"
                >
                    <span className="material-symbols-outlined text-[20px]">add</span>
                    Add Medicine
                </button>
            </div>

            {/* 2. KPI / SUMMARY STRIP */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <StatCard
                    title="Total Medicines"
                    value={stats.total}
                    icon="medication"
                />
                <StatCard
                    title="Active"
                    value={stats.active}
                    icon="check_circle"
                />
                <StatCard
                    title="Low Stock"
                    value={stats.lowStock}
                    icon="warning"
                />
                <StatCard
                    title="Categories"
                    value={stats.categories}
                    icon="category"
                />
            </div>

            {/* 3. LIST CONTROLS STRIP */}
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 px-4 py-3">
                <div className="flex items-center justify-between gap-4">
                    <h2 className="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                        Medicine List
                        <span className="px-2 py-0.5 text-xs font-medium bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded-full">
                            {totalItems}
                        </span>
                    </h2>
                    <div className="flex items-center gap-2">
                        <div className="relative">
                            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                                <span className="material-symbols-outlined text-[18px]">search</span>
                            </span>
                            <input
                                type="text"
                                placeholder="Search..."
                                value={search}
                                onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }}
                                className="w-44 pl-9 pr-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-1 focus:ring-blue-500"
                            />
                        </div>
                        <button className="p-2 rounded-lg border border-slate-200 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-700">
                            <span className="material-symbols-outlined text-[18px] text-slate-500">filter_list</span>
                        </button>
                        <select
                            value={categoryFilter}
                            onChange={(e) => { setCategoryFilter(e.target.value); setCurrentPage(1); }}
                            className="px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 text-slate-700 dark:text-slate-300"
                        >
                            <option value="">All Categories</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* 4. ENTITY TABLE */}
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
                {loading ? (
                    <div className="flex justify-center py-16">
                        <div className="animate-spin h-10 w-10 border-2 border-blue-600 border-t-transparent rounded-full"></div>
                    </div>
                ) : medicines.length === 0 ? (
                    <div className="py-16 text-center">
                        <span className="material-symbols-outlined text-5xl text-slate-300 dark:text-slate-600 mb-3">medication</span>
                        <h3 className="text-lg font-medium text-slate-900 dark:text-white">No medicines found</h3>
                        <p className="text-slate-500 mt-1">Add items to your catalog to get started</p>
                        <button
                            onClick={() => navigate('/medicines/add')}
                            className="mt-4 px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-700"
                        >
                            Add Medicine
                        </button>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-slate-50 dark:bg-slate-900/50">
                                <tr>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Medicine</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase hidden md:table-cell">Manufacturer</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase hidden sm:table-cell">Type</th>
                                    <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 uppercase">MRP</th>
                                    <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 uppercase">Stock</th>
                                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 uppercase">Status</th>
                                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 uppercase">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                                {medicines.map((medicine) => (
                                    <tr key={medicine.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 group">
                                        <td className="px-4 py-2.5">
                                            <div className="flex items-center gap-2.5">
                                                <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm">
                                                    <span className="material-symbols-outlined text-[16px]">medication</span>
                                                </div>
                                                <div>
                                                    <p className="font-medium text-sm text-slate-900 dark:text-white">{medicine.name}</p>
                                                    <p className="text-xs text-slate-500">{medicine.generic_name}</p>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-4 py-2.5 text-sm text-slate-700 dark:text-slate-300 hidden md:table-cell">{medicine.manufacturer}</td>
                                        <td className="px-4 py-2.5 hidden sm:table-cell">
                                            <span className="capitalize text-sm text-slate-600 dark:text-slate-400">{medicine.medicine_type}</span>
                                        </td>
                                        <td className="px-4 py-2.5 text-right text-sm font-medium text-slate-900 dark:text-white">
                                            ₹{medicine.mrp.toFixed(2)}
                                        </td>
                                        <td className="px-4 py-2.5 text-right">
                                            <span className={`text-sm font-medium ${medicine.total_stock < 50 ? 'text-red-600' : 'text-slate-600 dark:text-slate-400'}`}>
                                                {medicine.total_stock.toLocaleString()}
                                            </span>
                                        </td>
                                        <td className="px-4 py-2.5 text-center">
                                            <span className={`px-2 py-0.5 rounded-full text-[11px] font-medium ${medicine.is_active
                                                ? 'bg-green-100/80 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                                                : 'bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-400'
                                                }`}>
                                                {medicine.is_active ? 'Active' : 'Inactive'}
                                            </span>
                                        </td>
                                        <td className="px-4 py-2.5">
                                            <div className="flex items-center justify-center gap-0.5 opacity-60 group-hover:opacity-100">
                                                <button
                                                    onClick={() => navigate(`/medicines/${medicine.id}/edit`)}
                                                    className="p-1.5 rounded hover:bg-slate-100 dark:hover:bg-slate-700"
                                                    title="Edit"
                                                >
                                                    <span className="material-symbols-outlined text-slate-400 text-[18px]">edit</span>
                                                </button>
                                                {canDelete && (
                                                    <button
                                                        onClick={() => handleDelete(medicine)}
                                                        className="p-1.5 rounded hover:bg-red-50 dark:hover:bg-red-900/20"
                                                        title="Delete"
                                                    >
                                                        <span className="material-symbols-outlined text-slate-400 hover:text-red-500 text-[18px]">delete</span>
                                                    </button>
                                                )}
                                            </div>
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
