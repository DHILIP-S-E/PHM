import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { medicinesApi, inventoryApi } from '../services/api';
import { useOperationalContext } from '../contexts/OperationalContext';

interface Medicine {
    id: string;
    name: string;
    generic_name: string;
    manufacturer: string;
    mrp: number;
    purchase_price: number;
}

interface Batch {
    id: string;
    batch_number: string;
    expiry_date: string;
    quantity: number;
    mrp: number;
}

export default function WarehouseStockEntry() {
    const navigate = useNavigate();
    const { activeEntity } = useOperationalContext();

    const [medicines, setMedicines] = useState<Medicine[]>([]);
    const [existingBatches, setExistingBatches] = useState<Batch[]>([]); // For convenience dropdown

    // Derived from context
    const warehouseId = activeEntity?.type === 'warehouse' ? activeEntity.id : '';
    const warehouseName = activeEntity?.type === 'warehouse' ? activeEntity.name : '';

    const [selectedMedicine, setSelectedMedicine] = useState('');
    // Batch is entered directly (created implicitly with stock)
    const [batchNumber, setBatchNumber] = useState('');
    const [expiryDate, setExpiryDate] = useState('');
    const [quantity, setQuantity] = useState('');
    // Rack fields - physical storage location
    const [rackName, setRackName] = useState('');  // e.g., "Painkillers Box", "Cold Medicines"
    const [rackNumber, setRackNumber] = useState('');  // e.g., "R-01", "R-2A"
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });
    const [recentEntries, setRecentEntries] = useState<any[]>([]);
    const [selectedExistingBatch, setSelectedExistingBatch] = useState('');

    // Enforce Context
    useEffect(() => {
        if (!activeEntity || activeEntity.type !== 'warehouse') {
            navigate('/');
        }
    }, [activeEntity, navigate]);

    // Initialize
    useEffect(() => {
        if (activeEntity?.type === 'warehouse') {
            loadMedicines();
        }
    }, [activeEntity]);

    // Load batches when medicine changes
    useEffect(() => {
        if (selectedMedicine) {
            loadExistingBatches(selectedMedicine);
        } else {
            setExistingBatches([]);
        }
        // Reset batch fields when medicine changes
        setBatchNumber('');
        setExpiryDate('');
        setSelectedExistingBatch('');
    }, [selectedMedicine]);



    const loadMedicines = async () => {
        try {
            const response = await medicinesApi.list({ size: 100 });
            setMedicines(response.data.items || response.data);
        } catch (error) {
            console.error('Error loading medicines:', error);
        }
    };

    // Load existing batches for convenience (optional reuse)
    const loadExistingBatches = async (medicineId: string) => {
        try {
            const response = await medicinesApi.getBatches(medicineId);
            let batchesData: Batch[] = [];
            if (response.data) {
                if (Array.isArray(response.data)) {
                    batchesData = response.data;
                } else if (response.data.items && Array.isArray(response.data.items)) {
                    batchesData = response.data.items;
                } else if (response.data.data && Array.isArray(response.data.data)) {
                    batchesData = response.data.data;
                }
            }
            setExistingBatches(batchesData);
        } catch (error) {
            console.error('Error loading batches:', error);
            setExistingBatches([]);
        }
    };

    // When user selects an existing batch, populate the fields
    const handleExistingBatchSelect = (batchId: string) => {
        setSelectedExistingBatch(batchId);
        if (batchId) {
            const batch = existingBatches.find(b => b.id === batchId);
            if (batch) {
                setBatchNumber(batch.batch_number);
                setExpiryDate(batch.expiry_date);
            }
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        // Validation: batch_number, expiry_date, quantity are MANDATORY
        if (!warehouseId || !selectedMedicine || !batchNumber || !expiryDate || !quantity) {
            setMessage({ type: 'error', text: 'Please fill all required fields: Warehouse, Medicine, Batch Number, Expiry Date, and Quantity' });
            return;
        }

        setLoading(true);
        try {
            const stockData = {
                warehouse_id: warehouseId,
                medicine_id: selectedMedicine,
                batch_number: batchNumber,  // Batch created implicitly
                expiry_date: expiryDate,     // Batch created implicitly
                quantity: parseInt(quantity),
                rack_name: rackName || undefined,    // Physical storage - e.g., "Painkillers Box"
                rack_number: rackNumber || undefined  // Physical rack - e.g., "R-01"
            };

            await inventoryApi.stockEntry(stockData); // This creates stock + batch implicitly

            const medicine = medicines.find(m => m.id === selectedMedicine);

            setRecentEntries(prev => [{
                medicine: medicine?.name,
                batch: batchNumber,
                quantity: parseInt(quantity),
                rack: rackName ? `${rackName} (${rackNumber})` : rackNumber,
                timestamp: new Date().toLocaleTimeString()
            }, ...prev.slice(0, 9)]);

            setMessage({ type: 'success', text: 'Stock entry added successfully! Batch created/updated.' });
            setQuantity('');
            setRackName('');
            setRackNumber('');
            setBatchNumber('');
            setExpiryDate('');
            setSelectedExistingBatch('');
            // Reload batches to show the newly created one
            if (selectedMedicine) loadExistingBatches(selectedMedicine);
        } catch (error: any) {
            setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to add stock entry' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 lg:p-8 max-w-7xl mx-auto animate-fadeIn">
            <button
                onClick={() => navigate('/warehouses')}
                className="flex items-center gap-2 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white mb-6 transition-colors"
            >
                <span className="material-symbols-outlined text-[20px]">arrow_back</span>
                <span>Back to Warehouses</span>
            </button>

            <div className="mb-8">
                <h1 className="text-2xl lg:text-3xl font-bold text-slate-900 dark:text-white">📦 Warehouse Stock Entry</h1>
                <p className="text-slate-500 dark:text-slate-400 mt-1">Add new inventory items to your warehouse.</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm p-6">
                    <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
                        <span className="material-symbols-outlined text-primary">add_circle</span>
                        Add Stock
                    </h2>

                    {message.text && (
                        <div className={`p-4 rounded-xl mb-6 flex items-start gap-3 ${message.type === 'error'
                            ? 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800'
                            : 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800'
                            }`}>
                            <span className="material-symbols-outlined text-[20px] mt-0.5">
                                {message.type === 'error' ? 'error' : 'check_circle'}
                            </span>
                            <p>{message.text}</p>
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Warehouse Selector - ONLY visible to Super Admin */}
                        <div>
                            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Warehouse</label>
                            <div className="p-3 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl text-slate-700 dark:text-slate-300 font-medium flex items-center gap-2">
                                <span className="material-symbols-outlined text-slate-400">warehouse</span>
                                {warehouseName}
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Medicine *</label>
                            <select
                                value={selectedMedicine}
                                onChange={(e) => setSelectedMedicine(e.target.value)}
                                required
                                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 focus:ring-2 focus:ring-primary/50"
                            >
                                <option value="">Select Medicine</option>
                                {medicines.map(med => (
                                    <option key={med.id} value={med.id}>
                                        {med.name} - {med.manufacturer}
                                    </option>
                                ))}
                            </select>
                            {selectedMedicine && (() => {
                                const med = medicines.find(m => m.id === selectedMedicine);
                                return med ? (
                                    <div className="mt-3 p-3 bg-blue-50 dark:bg-blue-900/20 border border-blue-100 dark:border-blue-800 rounded-lg text-sm grid grid-cols-2 gap-2">
                                        <div className="flex justify-between"><span className="text-slate-500 dark:text-slate-400">Generic:</span> <span className="font-medium text-slate-900 dark:text-white">{med.generic_name}</span></div>
                                        <div className="flex justify-between"><span className="text-slate-500 dark:text-slate-400">MRP:</span> <span className="font-medium text-slate-900 dark:text-white">₹{med.mrp}</span></div>
                                    </div>
                                ) : null;
                            })()}
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Batch Number *</label>
                                <input
                                    type="text"
                                    value={batchNumber}
                                    onChange={(e) => setBatchNumber(e.target.value.toUpperCase())}
                                    placeholder="e.g., BATCH001"
                                    required
                                    disabled={!selectedMedicine}
                                    className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 disabled:opacity-50 font-mono"
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Expiry Date *</label>
                                <input
                                    type="date"
                                    value={expiryDate}
                                    onChange={(e) => setExpiryDate(e.target.value)}
                                    required
                                    disabled={!selectedMedicine}
                                    className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 disabled:opacity-50"
                                />
                            </div>
                        </div>

                        {/* Optional: Select from existing batches for convenience */}
                        {existingBatches.length > 0 && (
                            <div className="p-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-800 rounded-lg">
                                <label className="block text-xs font-medium text-amber-700 dark:text-amber-400 mb-2">Or select an existing batch to reuse details:</label>
                                <select
                                    value={selectedExistingBatch}
                                    onChange={(e) => handleExistingBatchSelect(e.target.value)}
                                    disabled={!selectedMedicine}
                                    className="w-full px-3 py-2 rounded-lg border border-amber-200 dark:border-amber-700 bg-white dark:bg-slate-900 text-sm"
                                >
                                    <option value="">-- Use new batch details above --</option>
                                    {existingBatches.map(batch => (
                                        <option key={batch.id} value={batch.id}>
                                            {batch.batch_number} (Exp: {batch.expiry_date})
                                        </option>
                                    ))}
                                </select>
                            </div>
                        )}

                        <div>
                            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Quantity *</label>
                            <input
                                type="number"
                                value={quantity}
                                onChange={(e) => setQuantity(e.target.value)}
                                placeholder="Enter quantity to add"
                                min="1"
                                required
                                className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900"
                            />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Rack / Box Name</label>
                                <input
                                    type="text"
                                    value={rackName}
                                    onChange={(e) => setRackName(e.target.value)}
                                    placeholder="e.g., Shelf A"
                                    className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Rack Number</label>
                                <input
                                    type="text"
                                    value={rackNumber}
                                    onChange={(e) => setRackNumber(e.target.value.toUpperCase())}
                                    placeholder="e.g., A1"
                                    className="w-full px-4 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900"
                                />
                            </div>
                        </div>

                        <button type="submit" className="w-full py-3 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl hover:shadow-lg disabled:opacity-50 transition-all" disabled={loading}>
                            {loading ? (
                                <span className="flex items-center justify-center gap-2">
                                    <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                                    Adding Stock...
                                </span>
                            ) : 'Add Stock Entry'}
                        </button>
                    </form>
                </div>

                <div className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 shadow-sm p-6 h-fit">
                    <h2 className="text-lg font-bold text-slate-900 dark:text-white mb-6 flex items-center gap-2">
                        <span className="material-symbols-outlined text-slate-500">history</span>
                        Recent Entries
                    </h2>

                    {recentEntries.length > 0 ? (
                        <ul className="space-y-4">
                            {recentEntries.map((entry, index) => (
                                <li key={index} className="flex justify-between items-start p-3 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-800 animate-fadeIn">
                                    <div className="space-y-1">
                                        <div className="font-medium text-slate-900 dark:text-white">{entry.medicine}</div>
                                        <div className="flex flex-wrap gap-2 text-xs">
                                            <span className="px-2 py-0.5 rounded bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-400">
                                                Batch: {entry.batch}
                                            </span>
                                            {entry.rack && (
                                                <span className="px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400">
                                                    📍 {entry.rack}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                    <div className="text-right">
                                        <div className="font-bold text-green-600">+ {entry.quantity}</div>
                                        <div className="text-xs text-slate-400 mt-1">{entry.timestamp}</div>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <div className="text-center py-12 text-slate-400 bg-slate-50 dark:bg-slate-900/30 rounded-xl border border-dashed border-slate-200 dark:border-slate-700">
                            <span className="material-symbols-outlined text-4xl mb-2 opacity-50">post_add</span>
                            <p>No recent entries</p>
                            <p className="text-sm opacity-75">Added stock will appear here</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
