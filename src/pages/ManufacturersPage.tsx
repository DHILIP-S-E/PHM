import { useState, useEffect } from 'react';
import { mastersApi } from '../services/api';
import PageLayout from '../components/PageLayout';
import Card from '../components/Card';
import Button from '../components/Button';
import Input from '../components/Input';
import Badge from '../components/Badge';
import Modal from '../components/Modal';

interface Manufacturer {
    id: string;
    code: string;
    name: string;
    description?: string;
    is_active: boolean;
}

export default function ManufacturersPage() {
    const [items, setItems] = useState<Manufacturer[]>([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [editing, setEditing] = useState<Manufacturer | null>(null);
    const [formData, setFormData] = useState({ code: '', name: '', description: '' });
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => { loadData(); }, []);

    const loadData = async () => {
        setLoading(true);
        try {
            const res = await mastersApi.listManufacturers();
            setItems(res.data || []);
        } catch (err) {
            console.error('Failed to load manufacturers:', err);
        } finally {
            setLoading(false);
        }
    };

    const openCreate = () => {
        setEditing(null);
        setFormData({ code: '', name: '', description: '' });
        setError('');
        setShowModal(true);
    };

    const openEdit = (item: Manufacturer) => {
        setEditing(item);
        setFormData({ code: item.code, name: item.name, description: item.description || '' });
        setError('');
        setShowModal(true);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!formData.code || !formData.name) {
            setError('Code and Name are required');
            return;
        }
        setSaving(true);
        setError('');
        try {
            if (editing) {
                await mastersApi.updateManufacturer(editing.id, formData);
            } else {
                await mastersApi.createManufacturer(formData);
            }
            setShowModal(false);
            loadData();
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to save');
        } finally {
            setSaving(false);
        }
    };

    const handleDelete = async (item: Manufacturer) => {
        if (!confirm(`Delete "${item.name}"?`)) return;
        try {
            await mastersApi.deleteManufacturer(item.id);
            loadData();
        } catch (err: any) {
            alert(err.response?.data?.detail || 'Failed to delete');
        }
    };

    return (
        <PageLayout
            title="Manufacturers"
            description="Manage medicine manufacturer masters"
            icon="factory"
            actions={
                <Button variant="primary" onClick={openCreate}>
                    <span className="material-symbols-outlined text-[20px] mr-2">add</span>
                    Add Manufacturer
                </Button>
            }
        >
            <Card className="!p-0">
                {loading ? (
                    <div className="flex items-center justify-center py-16">
                        <div className="spinner"></div>
                    </div>
                ) : items.length === 0 ? (
                    <div className="py-16 text-center">
                        <span className="material-symbols-outlined text-5xl text-slate-300 mb-3">factory</span>
                        <h3 className="text-lg font-medium text-slate-900 dark:text-white">No Manufacturers</h3>
                        <p className="text-slate-500 mt-1">Create medicine manufacturer masters</p>
                        <Button variant="primary" className="mt-4" onClick={openCreate}>
                            Add First Manufacturer
                        </Button>
                    </div>
                ) : (
                    <table className="w-full">
                        <thead className="bg-slate-50 dark:bg-slate-900/50">
                            <tr>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Code</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Name</th>
                                <th className="px-6 py-4 text-left text-xs font-semibold text-slate-500 uppercase">Description</th>
                                <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase">Status</th>
                                <th className="px-6 py-4 text-center text-xs font-semibold text-slate-500 uppercase">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                            {items.map((item) => (
                                <tr key={item.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50">
                                    <td className="px-6 py-4 font-mono text-sm font-medium text-primary">{item.code}</td>
                                    <td className="px-6 py-4 font-medium text-slate-900 dark:text-white">{item.name}</td>
                                    <td className="px-6 py-4 text-slate-500">{item.description || '-'}</td>
                                    <td className="px-6 py-4 text-center">
                                        <Badge variant={item.is_active ? 'success' : 'secondary'}>
                                            {item.is_active ? 'Active' : 'Inactive'}
                                        </Badge>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex justify-center gap-1">
                                            <Button variant="secondary" onClick={() => openEdit(item)} className="!p-1.5">
                                                <span className="material-symbols-outlined text-[18px]">edit</span>
                                            </Button>
                                            <Button variant="secondary" onClick={() => handleDelete(item)} className="!p-1.5 text-red-600">
                                                <span className="material-symbols-outlined text-[18px]">delete</span>
                                            </Button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </Card>

            <Modal isOpen={showModal} onClose={() => setShowModal(false)} title={editing ? 'Edit Manufacturer' : 'Add Manufacturer'}>
                <form onSubmit={handleSubmit} className="space-y-4">
                    {error && <div className="p-3 bg-red-50 rounded-xl text-red-600 text-sm">{error}</div>}
                    <Input
                        label="Code"
                        value={formData.code}
                        onChange={(e) => setFormData({ ...formData, code: e.target.value.toLowerCase() })}
                        placeholder="e.g., sunpharma"
                        required
                    />
                    <Input
                        label="Name"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        placeholder="e.g., Sun Pharmaceutical"
                        required
                    />
                    <Input
                        label="Description (Optional)"
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        placeholder="Manufacturer description"
                    />
                    <div className="flex justify-end gap-3 pt-4">
                        <Button variant="secondary" type="button" onClick={() => setShowModal(false)}>Cancel</Button>
                        <Button variant="primary" type="submit" loading={saving}>
                            {saving ? 'Saving...' : editing ? 'Update' : 'Create'}
                        </Button>
                    </div>
                </form>
            </Modal>
        </PageLayout>
    );
}
