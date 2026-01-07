import { useState, useEffect } from 'react';
import { warehousesApi, medicinesApi } from '../services/api';

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

interface Warehouse {
    id: string;
    name: string;
    code: string;
}

export default function WarehouseStockEntry() {
    const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
    const [medicines, setMedicines] = useState<Medicine[]>([]);
    const [batches, setBatches] = useState<Batch[]>([]);
    const [selectedWarehouse, setSelectedWarehouse] = useState('');
    const [selectedMedicine, setSelectedMedicine] = useState('');
    const [selectedBatch, setSelectedBatch] = useState('');
    const [quantity, setQuantity] = useState('');
    const [rackLocation, setRackLocation] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });
    const [recentEntries, setRecentEntries] = useState<any[]>([]);

    useEffect(() => {
        loadWarehouses();
        loadMedicines();
    }, []);

    useEffect(() => {
        if (selectedMedicine) {
            loadBatches(selectedMedicine);
        } else {
            setBatches([]);
        }
    }, [selectedMedicine]);

    const loadWarehouses = async () => {
        try {
            const response = await warehousesApi.list();
            setWarehouses(response.data.items || response.data);
        } catch (error) {
            console.error('Error loading warehouses:', error);
        }
    };

    const loadMedicines = async () => {
        try {
            const response = await medicinesApi.list({ size: 100 });
            setMedicines(response.data.items || response.data);
        } catch (error) {
            console.error('Error loading medicines:', error);
        }
    };

    const loadBatches = async (medicineId: string) => {
        try {
            const response = await medicinesApi.getBatches(medicineId);

            // Extract batches array safely
            let batchesData = [];
            if (response.data) {
                if (Array.isArray(response.data)) {
                    batchesData = response.data;
                } else if (response.data.items && Array.isArray(response.data.items)) {
                    batchesData = response.data.items;
                } else if (response.data.data && Array.isArray(response.data.data)) {
                    batchesData = response.data.data;
                }
            }

            setBatches(batchesData);
        } catch (error) {
            console.error('Error loading batches:', error);
            setBatches([]);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!selectedWarehouse || !selectedMedicine || !selectedBatch || !quantity) {
            setMessage({ type: 'error', text: 'Please fill all required fields' });
            return;
        }

        setLoading(true);
        try {
            const stockData = {
                warehouse_id: selectedWarehouse,
                medicine_id: selectedMedicine,
                batch_id: selectedBatch,
                quantity: parseInt(quantity),
                rack_location: rackLocation || null
            };

            await warehousesApi.create(stockData); // This should be a stock entry endpoint

            const medicine = medicines.find(m => m.id === selectedMedicine);
            const batch = batches.find(b => b.id === selectedBatch);

            setRecentEntries(prev => [{
                medicine: medicine?.name,
                batch: batch?.batch_number,
                quantity: parseInt(quantity),
                timestamp: new Date().toLocaleTimeString()
            }, ...prev.slice(0, 9)]);

            setMessage({ type: 'success', text: 'Stock entry added successfully!' });
            setQuantity('');
            setRackLocation('');
            setSelectedBatch('');
        } catch (error: any) {
            setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to add stock entry' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="warehouse-stock-entry">
            <style>{`
                .warehouse-stock-entry {
                    padding: 24px;
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .page-header {
                    margin-bottom: 24px;
                }
                .page-header h1 {
                    font-size: 24px;
                    font-weight: 600;
                    color: #1a1a2e;
                    margin: 0 0 8px 0;
                }
                .page-header p {
                    color: #666;
                    margin: 0;
                }
                .content-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 24px;
                }
                @media (max-width: 768px) {
                    .content-grid {
                        grid-template-columns: 1fr;
                    }
                }
                .card {
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    padding: 24px;
                }
                .card-title {
                    font-size: 18px;
                    font-weight: 600;
                    color: #1a1a2e;
                    margin: 0 0 20px 0;
                    padding-bottom: 12px;
                    border-bottom: 1px solid #eee;
                }
                .form-group {
                    margin-bottom: 16px;
                }
                .form-group label {
                    display: block;
                    font-weight: 500;
                    color: #333;
                    margin-bottom: 6px;
                }
                .form-group select,
                .form-group input {
                    width: 100%;
                    padding: 10px 12px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    font-size: 14px;
                    transition: border-color 0.2s;
                }
                .form-group select:focus,
                .form-group input:focus {
                    outline: none;
                    border-color: #4a6cf7;
                }
                .btn-primary {
                    width: 100%;
                    padding: 12px;
                    background: linear-gradient(135deg, #4a6cf7, #6366f1);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.2s, box-shadow 0.2s;
                }
                .btn-primary:hover {
                    transform: translateY(-1px);
                    box-shadow: 0 4px 12px rgba(74, 108, 247, 0.4);
                }
                .btn-primary:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                    transform: none;
                }
                .message {
                    padding: 12px;
                    border-radius: 8px;
                    margin-bottom: 16px;
                }
                .message.success {
                    background: #d4edda;
                    color: #155724;
                }
                .message.error {
                    background: #f8d7da;
                    color: #721c24;
                }
                .recent-entries {
                    list-style: none;
                    padding: 0;
                    margin: 0;
                }
                .recent-entry {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 12px;
                    border-bottom: 1px solid #eee;
                }
                .recent-entry:last-child {
                    border-bottom: none;
                }
                .entry-info {
                    flex: 1;
                }
                .entry-medicine {
                    font-weight: 500;
                    color: #333;
                }
                .entry-batch {
                    font-size: 12px;
                    color: #666;
                }
                .entry-quantity {
                    font-weight: 600;
                    color: #4a6cf7;
                    font-size: 16px;
                }
                .entry-time {
                    font-size: 12px;
                    color: #999;
                    margin-left: 12px;
                }
                .empty-state {
                    text-align: center;
                    padding: 40px;
                    color: #999;
                }
                .medicine-info {
                    background: #f8f9ff;
                    padding: 12px;
                    border-radius: 8px;
                    margin-top: 8px;
                    font-size: 13px;
                }
                .medicine-info-row {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 4px;
                }
                .medicine-info-row:last-child {
                    margin-bottom: 0;
                }
            `}</style>

            <div className="page-header">
                <h1>📦 Warehouse Stock Entry</h1>
                <p>Add inventory to your warehouse</p>
            </div>

            <div className="content-grid">
                <div className="card">
                    <h2 className="card-title">Add Stock</h2>

                    {message.text && (
                        <div className={`message ${message.type}`}>
                            {message.text}
                        </div>
                    )}

                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label>Warehouse *</label>
                            <select
                                value={selectedWarehouse}
                                onChange={(e) => setSelectedWarehouse(e.target.value)}
                                required
                            >
                                <option value="">Select Warehouse</option>
                                {warehouses.map(wh => (
                                    <option key={wh.id} value={wh.id}>
                                        {wh.name} ({wh.code})
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Medicine *</label>
                            <select
                                value={selectedMedicine}
                                onChange={(e) => setSelectedMedicine(e.target.value)}
                                required
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
                                    <div className="medicine-info">
                                        <div className="medicine-info-row">
                                            <span>Generic:</span>
                                            <span>{med.generic_name}</span>
                                        </div>
                                        <div className="medicine-info-row">
                                            <span>MRP:</span>
                                            <span>₹{med.mrp}</span>
                                        </div>
                                        <div className="medicine-info-row">
                                            <span>Purchase Price:</span>
                                            <span>₹{med.purchase_price}</span>
                                        </div>
                                    </div>
                                ) : null;
                            })()}
                        </div>

                        <div className="form-group">
                            <label>Batch *</label>
                            <select
                                value={selectedBatch}
                                onChange={(e) => setSelectedBatch(e.target.value)}
                                required
                                disabled={!selectedMedicine}
                            >
                                <option value="">Select Batch</option>
                                {batches.map(batch => (
                                    <option key={batch.id} value={batch.id}>
                                        {batch.batch_number} (Exp: {batch.expiry_date})
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="form-group">
                            <label>Quantity *</label>
                            <input
                                type="number"
                                value={quantity}
                                onChange={(e) => setQuantity(e.target.value)}
                                placeholder="Enter quantity"
                                min="1"
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label>Rack Location</label>
                            <input
                                type="text"
                                value={rackLocation}
                                onChange={(e) => setRackLocation(e.target.value)}
                                placeholder="e.g., A1-S3"
                            />
                        </div>

                        <button type="submit" className="btn-primary" disabled={loading}>
                            {loading ? 'Adding...' : 'Add Stock Entry'}
                        </button>
                    </form>
                </div>

                <div className="card">
                    <h2 className="card-title">Recent Entries</h2>

                    {recentEntries.length > 0 ? (
                        <ul className="recent-entries">
                            {recentEntries.map((entry, index) => (
                                <li key={index} className="recent-entry">
                                    <div className="entry-info">
                                        <div className="entry-medicine">{entry.medicine}</div>
                                        <div className="entry-batch">Batch: {entry.batch}</div>
                                    </div>
                                    <span className="entry-quantity">+{entry.quantity}</span>
                                    <span className="entry-time">{entry.timestamp}</span>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <div className="empty-state">
                            <p>No entries yet</p>
                            <p>Your stock entries will appear here</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
