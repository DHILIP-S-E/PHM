import { useState, useEffect } from 'react';
import { invoicesApi } from '../services/api';
import SearchBar from '../components/SearchBar';

interface Invoice {
    id: string;
    invoice_number: string;
    customer_name: string;
    shop_name: string;
    total_amount: number;
    payment_status: string;
    payment_method: string;
    created_at: string;
}

export default function InvoicesList() {
    const [invoices, setInvoices] = useState<Invoice[]>([]);
    const [loading, setLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState('');
    const [search, setSearch] = useState('');

    useEffect(() => { fetchInvoices(); }, [statusFilter, search]);

    const fetchInvoices = async () => {
        try {
            setLoading(true);
            const params: any = { status: statusFilter || undefined };
            if (search) params.search = search;
            const res = await invoicesApi.list(params);
            setInvoices(res.data?.items || res.data?.data || res.data || []);
        } catch (e) { console.error(e); }
        finally { setLoading(false); }
    };

    const formatCurrency = (v: number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(v);

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'paid': return 'bg-green-100 text-green-700';
            case 'pending': return 'bg-amber-100 text-amber-700';
            case 'cancelled': return 'bg-red-100 text-red-700';
            default: return 'bg-slate-100 text-slate-700';
        }
    };

    return (
        <div className="space-y-6">
            <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Invoices</h1>
                    <p className="text-slate-500">View and manage sales invoices</p>
                </div>
                <div className="flex items-center gap-3 flex-wrap">
                    <div className="min-w-[250px]">
                        <SearchBar
                            placeholder="Search invoices by number or customer..."
                            value={search}
                            onChange={setSearch}
                        />
                    </div>
                    <select
                        value={statusFilter}
                        onChange={(e) => setStatusFilter(e.target.value)}
                        className="px-4 py-2.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white"
                    >
                        <option value="">All Status</option>
                        <option value="paid">Paid</option>
                        <option value="pending">Pending</option>
                        <option value="cancelled">Cancelled</option>
                    </select>
                </div>
            </div>

            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden">
                {loading ? (
                    <div className="flex justify-center h-64 items-center"><div className="animate-spin h-8 w-8 border-2 border-blue-600 border-t-transparent rounded-full"></div></div>
                ) : (
                    <table className="w-full">
                        <thead className="bg-slate-50 dark:bg-slate-900/50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Invoice #</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Customer</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Shop</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Amount</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Date</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                            {invoices.map((inv) => (
                                <tr key={inv.id} className="hover:bg-slate-50 dark:hover:bg-slate-900/30">
                                    <td className="px-6 py-4 font-mono text-sm text-slate-900 dark:text-white">{inv.invoice_number}</td>
                                    <td className="px-6 py-4 text-slate-700 dark:text-slate-300">{inv.customer_name || 'Walk-in'}</td>
                                    <td className="px-6 py-4 text-slate-500">{inv.shop_name || 'N/A'}</td>
                                    <td className="px-6 py-4 font-semibold text-slate-900 dark:text-white">{formatCurrency(inv.total_amount)}</td>
                                    <td className="px-6 py-4"><span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(inv.payment_status)}`}>{inv.payment_status}</span></td>
                                    <td className="px-6 py-4 text-sm text-slate-500">{new Date(inv.created_at).toLocaleDateString()}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
}
