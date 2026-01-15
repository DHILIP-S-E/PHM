import { useState, useEffect } from 'react';
import { employeesApi } from '../services/api';
import { DepartmentSelect, DesignationSelect, ShopSelect, EmploymentTypeSelect, GenderSelect } from '../components/MasterSelect';
import { useUser } from '../contexts/UserContext';
import StatCard from '../components/StatCard';
import SearchBar from '../components/SearchBar';

interface Employee {
    id: string;
    name: string;
    employee_code?: string;
    email?: string;
    phone: string;
    department: string;
    designation: string;
    employment_type?: string;
    salary: number;
    status: string;
    shop_id?: string;
    shop_name?: string;
    date_of_joining?: string;
    gender?: string;
}

interface EmployeeForm {
    name: string;
    email: string;
    phone: string;
    department: string;
    designation: string;
    employment_type: string;
    salary: number;
    shop_id: string;
    date_of_joining: string;
    address: string;
    emergency_contact: string;
    gender: string;
}

const emptyForm: EmployeeForm = {
    name: '',
    email: '',
    phone: '',
    department: 'operations', // Default changed from pharmacy
    designation: '',
    employment_type: 'full_time',
    salary: 0,
    shop_id: '',
    date_of_joining: new Date().toISOString().split('T')[0],
    address: '',
    emergency_contact: '',
    gender: '',
};

export default function EmployeesList() {
    const { user } = useUser();
    const [employees, setEmployees] = useState<Employee[]>([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [deptFilter, setDeptFilter] = useState('');
    const [currentPage, setCurrentPage] = useState(1);
    const [totalItems, setTotalItems] = useState(0);
    const pageSize = 10;

    // Modal states
    const [showModal, setShowModal] = useState(false);
    const [editingEmployee, setEditingEmployee] = useState<Employee | null>(null);
    const [formData, setFormData] = useState<EmployeeForm>(emptyForm);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState('');

    const isWarehouseAdmin = user?.role === 'warehouse_admin';

    useEffect(() => {
        fetchEmployees();
    }, [deptFilter, currentPage, search]);

    const fetchEmployees = async () => {
        try {
            setLoading(true);
            const params: any = { page: currentPage, size: pageSize };
            if (search) params.search = search;
            if (deptFilter) params.department = deptFilter;

            const res = await employeesApi.list(params);
            setEmployees(res.data.items || res.data.data || res.data || []);
            setTotalItems(res.data.total || res.data.length || 0);
        } catch (e) {
            console.error(e);
            setEmployees([]);
        } finally {
            setLoading(false);
        }
    };

    const openCreateModal = () => {
        setEditingEmployee(null);
        setFormData({
            ...emptyForm,
            department: isWarehouseAdmin ? 'operations' : 'pharmacy',
        });
        setError('');
        setShowModal(true);
    };

    const openEditModal = async (employee: Employee) => {
        try {
            const response = await employeesApi.get(employee.id);
            const data = response.data;
            setEditingEmployee(employee);
            setFormData({
                name: data.name || '',
                email: data.email || '',
                phone: data.phone || '',
                department: data.department || (isWarehouseAdmin ? 'operations' : 'pharmacy'),
                designation: data.designation || '',
                employment_type: data.employment_type || 'full_time',
                salary: data.salary || 0,
                shop_id: data.shop_id || '',
                date_of_joining: data.date_of_joining?.split('T')[0] || '',
                address: data.address || '',
                emergency_contact: data.emergency_contact || '',
                gender: data.gender || '',
            });
            setError('');
            setShowModal(true);
        } catch (err) {
            console.error('Failed to fetch employee details:', err);
            alert('Failed to load employee details');
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');

        if (!formData.name || !formData.phone || !formData.department) {
            setError('Please fill in all required fields (Name, Phone, Department)');
            return;
        }

        if (!formData.salary || formData.salary <= 0) {
            setError('Please enter a valid salary amount');
            return;
        }

        setSaving(true);
        try {
            // Prepare payload - convert empty strings to null/undefined for optional fields
            const payload: any = {
                name: formData.name,
                phone: formData.phone,
                department: formData.department,
                designation: formData.designation || undefined,
                employment_type: formData.employment_type,
                date_of_joining: formData.date_of_joining,
                basic_salary: Number(formData.salary) || undefined, // Backend expects 'basic_salary'
                email: formData.email || undefined,
                gender: formData.gender || undefined,
                address: formData.address || undefined,
                emergency_contact: formData.emergency_contact || undefined,
                shop_id: formData.shop_id || undefined,
            };

            if (editingEmployee) {
                await employeesApi.update(editingEmployee.id, payload);
            } else {
                await employeesApi.create(payload);
            }
            setShowModal(false);
            fetchEmployees();
        } catch (err: any) {
            console.error('Failed to save employee:', err);

            // Handle Pydantic validation errors (422)
            let errorMessage = 'Failed to save employee';
            if (err.response?.data?.detail) {
                const detail = err.response.data.detail;

                // If detail is an array of validation errors
                if (Array.isArray(detail)) {
                    errorMessage = detail.map((e: any) => {
                        const field = e.loc?.join('.') || 'Unknown field';
                        return `${field}: ${e.msg}`;
                    }).join(', ');
                } else if (typeof detail === 'string') {
                    errorMessage = detail;
                } else {
                    errorMessage = JSON.stringify(detail);
                }
            }

            setError(errorMessage);
        } finally {
            setSaving(false);
        }
    };

    const formatCurrency = (v: number) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(v);
    const totalPages = Math.ceil(totalItems / pageSize);

    // Calculate stats
    const stats = {
        total: employees.length,
        active: employees.filter(e => e.status === 'active').length,
        inactive: employees.filter(e => e.status === 'inactive').length,
        onLeave: employees.filter(e => e.status === 'on_leave').length
    };

    return (
        <div className="space-y-6">
            {/* 1. PAGE HEADER */}
            <div className="flex justify-between items-start">
                <div>
                    <h1 className="text-2xl font-bold text-slate-900 dark:text-white">Employees</h1>
                    <p className="text-slate-500 dark:text-slate-400 mt-1">Manage staff and payroll</p>
                </div>
                <button
                    onClick={openCreateModal}
                    className="flex items-center gap-2 px-4 py-2.5 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 shadow-lg shadow-blue-500/30 transition-all"
                >
                    <span className="material-symbols-outlined text-[20px]">add</span>
                    Add Employee
                </button>
            </div>

            {/* 2. KPI / SUMMARY STRIP */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <StatCard
                    title="Total Employees"
                    value={totalItems}
                    icon="badge"
                />
                <StatCard
                    title="Active"
                    value={stats.active}
                    icon="check_circle"
                    change="+5% vs last month"
                    changeType="up"
                />
                <StatCard
                    title="Inactive"
                    value={stats.inactive}
                    icon="cancel"
                />
                <StatCard
                    title="On Leave"
                    value={stats.onLeave}
                    icon="event_busy"
                />
            </div>

            {/* 3. LIST CONTROLS STRIP */}
            <div className="bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 px-4 py-3">
                <div className="flex items-center justify-between gap-4">
                    <h2 className="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                        Employee List
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
                            value={deptFilter}
                            onChange={(e) => { setDeptFilter(e.target.value); setCurrentPage(1); }}
                            className="px-3 py-2 text-sm rounded-lg border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-900 text-slate-700 dark:text-slate-300"
                        >
                            <option value="">All Depts</option>
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
                ) : employees.length === 0 ? (
                    <div className="py-16 text-center">
                        <span className="material-symbols-outlined text-5xl text-slate-300 dark:text-slate-600 mb-3">badge</span>
                        <h3 className="text-lg font-medium text-slate-900 dark:text-white">No employees found</h3>
                        <p className="text-slate-500 mt-1">Add your first employee to get started</p>
                        <button
                            onClick={openCreateModal}
                            className="mt-4 px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-700"
                        >
                            Add Employee
                        </button>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-slate-50 dark:bg-slate-900/50">
                                <tr>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Employee</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Department</th>
                                    <th className="px-4 py-3 text-left text-xs font-semibold text-slate-500 uppercase">Designation</th>
                                    <th className="px-4 py-3 text-right text-xs font-semibold text-slate-500 uppercase">Salary</th>
                                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 uppercase">Status</th>
                                    <th className="px-4 py-3 text-center text-xs font-semibold text-slate-500 uppercase">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-200 dark:divide-slate-700">
                                {employees.map((emp) => (
                                    <tr key={emp.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 group">
                                        <td className="px-4 py-2.5">
                                            <div className="flex items-center gap-2.5">
                                                <div className="w-8 h-8 rounded-full bg-violet-500 flex items-center justify-center text-white text-sm">
                                                    {emp.name.charAt(0)}
                                                </div>
                                                <div>
                                                    <p className="font-medium text-sm text-slate-900 dark:text-white">{emp.name}</p>
                                                    <p className="text-xs text-slate-500">{emp.phone}</p>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-4 py-2.5">
                                            <span className="px-2 py-0.5 rounded-full text-[11px] font-medium bg-blue-100/80 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 capitalize">
                                                {emp.department}
                                            </span>
                                        </td>
                                        <td className="px-4 py-2.5 text-sm text-slate-600 dark:text-slate-400">{emp.designation || 'N/A'}</td>
                                        <td className="px-4 py-2.5 text-right text-sm font-medium text-slate-900 dark:text-white">
                                            {formatCurrency(emp.salary || 0)}
                                        </td>
                                        <td className="px-4 py-2.5 text-center">
                                            <span className={`px-2 py-0.5 rounded-full text-[11px] font-medium ${emp.status === 'active'
                                                ? 'bg-green-100/80 text-green-700 dark:bg-green-900/30 dark:text-green-400'
                                                : 'bg-red-100/80 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                                                }`}>
                                                {emp.status || 'Active'}
                                            </span>
                                        </td>
                                        <td className="px-4 py-2.5">
                                            <div className="flex items-center justify-center opacity-60 group-hover:opacity-100">
                                                <button
                                                    onClick={() => openEditModal(emp)}
                                                    className="p-1.5 rounded hover:bg-slate-100 dark:hover:bg-slate-700"
                                                    title="Edit"
                                                >
                                                    <span className="material-symbols-outlined text-slate-400 text-[18px]">edit</span>
                                                </button>
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

            {/* Create/Edit Modal */}
            {showModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white dark:bg-slate-800 rounded-xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-auto">
                        <div className="p-6 border-b border-slate-200 dark:border-slate-700">
                            <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                                {editingEmployee ? 'Edit Employee' : 'Add New Employee'}
                            </h2>
                        </div>

                        <form onSubmit={handleSubmit}>
                            <div className="p-6 space-y-4">
                                {error && (
                                    <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-700 dark:text-red-300 text-sm">
                                        {error}
                                    </div>
                                )}

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Full Name *</label>
                                        <input
                                            type="text"
                                            value={formData.name}
                                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                            required
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Phone *</label>
                                        <input
                                            type="tel"
                                            value={formData.phone}
                                            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                            required
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Email</label>
                                        <input
                                            type="email"
                                            value={formData.email}
                                            onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Date of Joining</label>
                                        <input
                                            type="date"
                                            value={formData.date_of_joining}
                                            onChange={(e) => setFormData({ ...formData, date_of_joining: e.target.value })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Type</label>
                                        <EmploymentTypeSelect
                                            value={formData.employment_type}
                                            onChange={(val) => setFormData({ ...formData, employment_type: val })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Gender</label>
                                        <GenderSelect
                                            value={formData.gender}
                                            onChange={(val) => setFormData({ ...formData, gender: val })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Department *</label>
                                        <DepartmentSelect
                                            value={formData.department}
                                            onChange={(val) => setFormData({ ...formData, department: val })}
                                            required
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                        />
                                    </div>
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Designation</label>
                                        <DesignationSelect
                                            value={formData.designation}
                                            onChange={(val) => setFormData({ ...formData, designation: val })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                        />
                                    </div>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Monthly Salary (₹)</label>
                                        <input
                                            type="number"
                                            value={formData.salary}
                                            onChange={(e) => setFormData({ ...formData, salary: parseFloat(e.target.value) || 0 })}
                                            className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                        />
                                    </div>
                                    {/* Hide Shop selection for Warehouse Admins as they hire for their warehouse */}
                                    {!isWarehouseAdmin && (
                                        <div>
                                            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Assigned Shop</label>
                                            <ShopSelect
                                                value={formData.shop_id}
                                                onChange={(val) => setFormData({ ...formData, shop_id: val })}
                                                className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                            />
                                        </div>
                                    )}
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Address</label>
                                    <textarea
                                        value={formData.address}
                                        onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                                        className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                        rows={2}
                                    />
                                </div>

                                <div>
                                    <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Emergency Contact</label>
                                    <input
                                        type="tel"
                                        value={formData.emergency_contact}
                                        onChange={(e) => setFormData({ ...formData, emergency_contact: e.target.value })}
                                        className="w-full px-3 py-2 rounded-lg border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-900"
                                    />
                                </div>
                            </div>

                            <div className="p-6 border-t border-slate-200 dark:border-slate-700 flex justify-end gap-3">
                                <button
                                    type="button"
                                    onClick={() => setShowModal(false)}
                                    className="px-4 py-2 border border-slate-200 dark:border-slate-600 rounded-lg font-medium hover:bg-slate-50 dark:hover:bg-slate-700"
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    disabled={saving}
                                    className="px-4 py-2 bg-primary text-white rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
                                >
                                    {saving ? 'Saving...' : editingEmployee ? 'Update Employee' : 'Add Employee'}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}
