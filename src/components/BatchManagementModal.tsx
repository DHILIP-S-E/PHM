import { useState, useEffect } from 'react';
import { medicinesApi } from '../services/api';

interface Batch {
    id: string;
    batch_number: string;
    manufacturing_date?: string;
    expiry_date: string;
    quantity: number;
    purchase_price: number;
    mrp: number;
    is_expired: boolean;
    days_to_expiry: number;
    created_at: string;
}

interface BatchManagementModalProps {
    medicineId: string;
    medicineName: string;
    onClose: () => void;
}

export default function BatchManagementModal({ medicineId, medicineName, onClose }: BatchManagementModalProps) {
    const [batches, setBatches] = useState<Batch[]>([]);
    const [loading, setLoading] = useState(true);
    const [showAddForm, setShowAddForm] = useState(false);
    const [saving, setSaving] = useState(false);

    const [formData, setFormData] = useState({
        batch_number: '',
        manufacturing_date: '',
        expiry_date: '',
        quantity: 0,
        purchase_price: 0,
        mrp: 0,
    });

    useEffect(() => {
        fetchBatches();
    }, [medicineId]);

    const fetchBatches = async () => {
        try {
            setLoading(true);
            console.log('Fetching batches for medicine:', medicineId);
            const response = await medicinesApi.getBatches(medicineId);
            setBatches(response.data.batches || []);
        } catch (error) {
            console.error('Failed to fetch batches:', error);
            window.toast?.error('Failed to load batches');
            setBatches([]);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!formData.batch_number || !formData.expiry_date || !formData.quantity) {
            window.toast?.error('Please fill all required fields');
            return;
        }

        setSaving(true);
        try {
            await medicinesApi.createBatch(medicineId, formData);
            window.toast?.success('Batch created successfully');
            setShowAddForm(false);
            setFormData({
                batch_number: '',
                manufacturing_date: '',
                expiry_date: '',
                quantity: 0,
                purchase_price: 0,
                mrp: 0,
            });
            fetchBatches();
        } catch (error: any) {
            console.error('Failed to create batch:', error);

            // Extract detailed error message from backend
            let errorMessage = 'Failed to create batch';

            if (error.response?.data) {
                // FastAPI validation errors
                if (error.response.data.detail) {
                    if (Array.isArray(error.response.data.detail)) {
                        // Pydantic validation errors
                        errorMessage = error.response.data.detail
                            .map((err: any) => `${err.loc.join('.')}: ${err.msg}`)
                            .join(', ');
                    } else if (typeof error.response.data.detail === 'string') {
                        errorMessage = error.response.data.detail;
                    }
                } else if (error.response.data.message) {
                    errorMessage = error.response.data.message;
                }
            } else if (error.message) {
                errorMessage = error.message;
            }

            window.toast?.error(errorMessage);
        } finally {
            setSaving(false);
        }
    };

    const getExpiryBadge = (batch: Batch) => {
        if (batch.is_expired) {
            return <span className="px-2 py-1 text-xs font-medium bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400 rounded-full">Expired</span>;
        }
        if (batch.days_to_expiry <= 30) {
            return <span className="px-2 py-1 text-xs font-medium bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400 rounded-full">Expiring Soon</span>;
        }
        return <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 rounded-full">Active</span>;
    };

    const formatDate = (dateString: string) => {
        if (!dateString) return '-';
        return new Date(dateString).toLocaleDateString('en-IN');
    };

    return (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-fadeIn" onClick={onClose}>
            <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl w-full max-w-5xl max-h-[90vh] overflow-hidden animate-scaleIn" onClick={(e) => e.stopPropagation()}>
                {/* Header */}
                <div className="p-6 border-b border-slate-200 dark:border-slate-700 flex items-center justify-between">
                    <div>
                        <h2 className="text-xl font-bold text-slate-900 dark:text-white">Batch Management</h2>
                        <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">{medicineName}</p>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
                    >
                        <span className="material-symbols-outlined text-slate-500">close</span>
                    </button>
                </div>

                {/* Content */}
                <div className="p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
                    {/* Add Batch Button */}
                    {!showAddForm && (
                        <button
                            onClick={() => setShowAddForm(true)}
                            className="mb-4 flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-xl font-semibold hover:bg-blue-700 shadow-lg shadow-blue-500/30 transition-all"
                        >
                            <span className="material-symbols-outlined text-[20px]">add</span>
                            Add New Batch
                        </button>
                    )}

                    {/* Add Batch Form */}
                    {showAddForm && (
                        <div className="mb-6 p-4 bg-slate-50 dark:bg-slate-900/50 rounded-xl border border-slate-200 dark:border-slate-700">
                            <h3 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">Add New Batch</h3>
                            <form onSubmit={handleSubmit} className="space-y-4">
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                                            Batch Number *
                                        </label>
                                        <input
                                            type="text"
                                            value={formData.batch_number}
                                            onChange={(e) => setFormData({ ...formData, batch_number: e.target.value })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
                                            placeholder="LOT-2024-001"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                                            Quantity *
                                        </label>
                                        <input
                                            type="number"
                                            value={formData.quantity}
                                            onChange={(e) => setFormData({ ...formData, quantity: parseInt(e.target.value) || 0 })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
                                            min="1"
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                                            Manufacturing Date
                                        </label>
                                        <input
                                            type="date"
                                            value={formData.manufacturing_date}
                                            onChange={(e) => setFormData({ ...formData, manufacturing_date: e.target.value })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                                            Expiry Date *
                                        </label>
                                        <input
                                            type="date"
                                            value={formData.expiry_date}
                                            onChange={(e) => setFormData({ ...formData, expiry_date: e.target.value })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                                            Purchase Price (₹)
                                        </label>
                                        <input
                                            type="number"
                                            step="0.01"
                                            value={formData.purchase_price}
                                            onChange={(e) => setFormData({ ...formData, purchase_price: parseFloat(e.target.value) || 0 })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">
                                            MRP (₹)
                                        </label>
                                        <input
                                            type="number"
                                            step="0.01"
                                            value={formData.mrp}
                                            onChange={(e) => setFormData({ ...formData, mrp: parseFloat(e.target.value) || 0 })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white"
                                        />
                                    </div>
                                </div>

                                <div className="flex gap-3">
                                    <button
                                        type="submit"
                                        disabled={saving}
                                        className="px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
                                    >
                                        {saving ? 'Creating...' : 'Create Batch'}
                                    </button>
                                    <button
                                        type="button"
                                        onClick={() => setShowAddForm(false)}
                                        className="px-4 py-2 border border-slate-200 dark:border-slate-600 rounded-lg font-medium hover:bg-slate-50 dark:hover:bg-slate-700"
                                    >
                                        Cancel
                                    </button>
                                </div>
                            </form>
                        </div>
                    )}

                    {/* Batches List */}
                    {loading ? (
                        <div className="flex items-center justify-center py-12">
                            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary"></div>
                        </div>
                    ) : batches.length === 0 ? (
                        <div className="text-center py-12">
                            <span className="material-symbols-outlined text-5xl text-slate-300 dark:text-slate-600 mb-3">inventory_2</span>
                            <h3 className="text-lg font-medium text-slate-900 dark:text-white">No batches found</h3>
                            <p className="text-slate-500 dark:text-slate-400 mt-1">Add batches to track inventory and expiry</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full">
                                <thead className="bg-slate-50 dark:bg-slate-900/50">
                                    <tr>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Batch #</th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Mfg Date</th>
                                        <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Expiry Date</th>
                                        <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Quantity</th>
                                        <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Purchase Price</th>
                                        <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">MRP</th>
                                        <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase">Status</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                                    {batches.map((batch) => (
                                        <tr key={batch.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                                            <td className="px-4 py-3 font-mono text-sm text-slate-900 dark:text-white">{batch.batch_number}</td>
                                            <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-400">{formatDate(batch.manufacturing_date || '')}</td>
                                            <td className="px-4 py-3 text-sm text-slate-600 dark:text-slate-400">
                                                <div>
                                                    <div>{formatDate(batch.expiry_date)}</div>
                                                    {!batch.is_expired && (
                                                        <div className="text-xs text-slate-500">({batch.days_to_expiry} days left)</div>
                                                    )}
                                                </div>
                                            </td>
                                            <td className="px-4 py-3 text-right font-medium text-slate-900 dark:text-white">{batch.quantity}</td>
                                            <td className="px-4 py-3 text-right text-slate-600 dark:text-slate-400">₹{batch.purchase_price.toFixed(2)}</td>
                                            <td className="px-4 py-3 text-right text-slate-600 dark:text-slate-400">₹{batch.mrp.toFixed(2)}</td>
                                            <td className="px-4 py-3 text-center">{getExpiryBadge(batch)}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>

                {/* Footer */}
                <div className="p-6 border-t border-slate-200 dark:border-slate-700 flex justify-between items-center">
                    <p className="text-sm text-slate-500">
                        Total Batches: <span className="font-semibold text-slate-900 dark:text-white">{batches.length}</span>
                    </p>
                    <button
                        onClick={onClose}
                        className="px-4 py-2 bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg font-medium hover:bg-slate-200 dark:hover:bg-slate-600"
                    >
                        Close
                    </button>
                </div>
            </div>
        </div>
    );
}
