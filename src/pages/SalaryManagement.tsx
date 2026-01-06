import { useState, useEffect } from 'react';
import { employeesApi } from '../services/api';

interface Employee {
    id: string;
    employee_code: string;
    name: string;
    designation: string;
    department: string;
    basic_salary: number;
}

interface SalaryRecord {
    id: string;
    employee_id: string;
    month: number;
    year: number;
    basic_salary: number;
    hra: number;
    allowances: number;
    deductions: number;
    pf_deduction: number;
    esi_deduction: number;
    tax_deduction: number;
    bonus: number;
    gross_salary: number;
    net_salary: number;
    is_paid: boolean;
}

export default function SalaryManagement() {
    const [employees, setEmployees] = useState<Employee[]>([]);
    const [salaryRecords, setSalaryRecords] = useState<SalaryRecord[]>([]);
    const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
    const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());
    const [loading, setLoading] = useState(true);
    const [processing, setProcessing] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });

    useEffect(() => {
        loadEmployees();
    }, []);

    useEffect(() => {
        if (employees.length > 0) {
            loadSalaryRecords();
        }
    }, [selectedMonth, selectedYear, employees]);

    const loadEmployees = async () => {
        try {
            const response = await employeesApi.list({ size: 100 });
            setEmployees(response.data.items || response.data);
        } catch (error) {
            console.error('Error loading employees:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadSalaryRecords = async () => {
        // In a real implementation, this would fetch from the API
        // For now, we'll generate placeholder data
        const records: SalaryRecord[] = employees.map(emp => ({
            id: `sal-${emp.id}`,
            employee_id: emp.id,
            month: selectedMonth,
            year: selectedYear,
            basic_salary: emp.basic_salary || 25000,
            hra: (emp.basic_salary || 25000) * 0.4,
            allowances: 5000,
            deductions: 0,
            pf_deduction: (emp.basic_salary || 25000) * 0.12,
            esi_deduction: (emp.basic_salary || 25000) * 0.0075,
            tax_deduction: 0,
            bonus: 0,
            gross_salary: (emp.basic_salary || 25000) * 1.4 + 5000,
            net_salary: ((emp.basic_salary || 25000) * 1.4 + 5000) - ((emp.basic_salary || 25000) * 0.1275),
            is_paid: false
        }));
        setSalaryRecords(records);
    };

    const processSalary = async () => {
        setProcessing(true);
        try {
            await employeesApi.processSalary({
                month: selectedMonth,
                year: selectedYear
            });
            setMessage({ type: 'success', text: `Salary processed for ${getMonthName(selectedMonth)} ${selectedYear}` });
            loadSalaryRecords();
        } catch (error: any) {
            setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to process salary' });
        } finally {
            setProcessing(false);
        }
    };

    const getMonthName = (month: number) => {
        return new Date(2000, month - 1).toLocaleString('default', { month: 'long' });
    };

    const formatCurrency = (amount: number) => {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            maximumFractionDigits: 0
        }).format(amount);
    };

    const totalGross = salaryRecords.reduce((sum, r) => sum + r.gross_salary, 0);
    const totalNet = salaryRecords.reduce((sum, r) => sum + r.net_salary, 0);
    const totalPF = salaryRecords.reduce((sum, r) => sum + r.pf_deduction, 0);
    const totalESI = salaryRecords.reduce((sum, r) => sum + r.esi_deduction, 0);

    return (
        <div className="salary-management">
            <style>{`
                .salary-management {
                    padding: 24px;
                    max-width: 1400px;
                    margin: 0 auto;
                }
                .page-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 24px;
                }
                .page-header h1 {
                    font-size: 24px;
                    font-weight: 600;
                    color: #1a1a2e;
                    margin: 0;
                }
                .header-actions {
                    display: flex;
                    gap: 12px;
                }
                .btn-process {
                    padding: 12px 24px;
                    background: linear-gradient(135deg, #10b981, #059669);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .btn-process:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
                }
                .controls-card {
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    padding: 20px;
                    margin-bottom: 24px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 16px;
                }
                .period-selector {
                    display: flex;
                    gap: 12px;
                    align-items: center;
                }
                .period-selector select {
                    padding: 10px 16px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    font-size: 14px;
                }
                .summary-stats {
                    display: flex;
                    gap: 32px;
                }
                .summary-stat {
                    text-align: right;
                }
                .summary-stat-value {
                    font-size: 20px;
                    font-weight: 700;
                    color: #1a1a2e;
                }
                .summary-stat-label {
                    font-size: 12px;
                    color: #666;
                }
                .salary-table {
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                    overflow: hidden;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                }
                th, td {
                    padding: 14px 12px;
                    text-align: left;
                    border-bottom: 1px solid #eee;
                    font-size: 14px;
                }
                th {
                    background: #f8f9ff;
                    font-weight: 600;
                    color: #333;
                    font-size: 12px;
                    text-transform: uppercase;
                }
                tr:hover {
                    background: #fafbff;
                }
                .employee-info {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                .employee-avatar {
                    width: 36px;
                    height: 36px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #4a6cf7, #6366f1);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                    font-size: 14px;
                }
                .employee-name {
                    font-weight: 500;
                    color: #333;
                }
                .employee-code {
                    font-size: 11px;
                    color: #888;
                }
                .amount-cell {
                    font-family: 'Consolas', monospace;
                    text-align: right;
                }
                .amount-cell.earnings {
                    color: #10b981;
                }
                .amount-cell.deductions {
                    color: #ef4444;
                }
                .amount-cell.net {
                    font-weight: 700;
                    color: #4a6cf7;
                }
                .status-badge {
                    padding: 4px 10px;
                    border-radius: 20px;
                    font-size: 11px;
                    font-weight: 600;
                }
                .status-badge.paid {
                    background: #d4edda;
                    color: #155724;
                }
                .status-badge.pending {
                    background: #fff3cd;
                    color: #856404;
                }
                .message {
                    padding: 12px 20px;
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
                .loading {
                    text-align: center;
                    padding: 60px;
                    color: #666;
                }
                .action-btn {
                    padding: 6px 12px;
                    border: 1px solid #ddd;
                    background: white;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 12px;
                }
                .action-btn:hover {
                    background: #f5f5f5;
                }
            `}</style>

            <div className="page-header">
                <h1>💰 Salary Management</h1>
                <div className="header-actions">
                    <button
                        className="btn-process"
                        onClick={processSalary}
                        disabled={processing}
                    >
                        {processing ? '⏳ Processing...' : '📊 Process Salary'}
                    </button>
                </div>
            </div>

            {message.text && (
                <div className={`message ${message.type}`}>
                    {message.text}
                </div>
            )}

            <div className="controls-card">
                <div className="period-selector">
                    <span>Period:</span>
                    <select value={selectedMonth} onChange={(e) => setSelectedMonth(Number(e.target.value))}>
                        {Array.from({ length: 12 }, (_, i) => (
                            <option key={i + 1} value={i + 1}>{getMonthName(i + 1)}</option>
                        ))}
                    </select>
                    <select value={selectedYear} onChange={(e) => setSelectedYear(Number(e.target.value))}>
                        {Array.from({ length: 5 }, (_, i) => (
                            <option key={i} value={new Date().getFullYear() - i}>
                                {new Date().getFullYear() - i}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="summary-stats">
                    <div className="summary-stat">
                        <div className="summary-stat-value">{formatCurrency(totalGross)}</div>
                        <div className="summary-stat-label">Total Gross</div>
                    </div>
                    <div className="summary-stat">
                        <div className="summary-stat-value" style={{ color: '#ef4444' }}>{formatCurrency(totalPF + totalESI)}</div>
                        <div className="summary-stat-label">Total Deductions</div>
                    </div>
                    <div className="summary-stat">
                        <div className="summary-stat-value" style={{ color: '#10b981' }}>{formatCurrency(totalNet)}</div>
                        <div className="summary-stat-label">Total Net Payable</div>
                    </div>
                </div>
            </div>

            {loading ? (
                <div className="loading">Loading salary data...</div>
            ) : (
                <div className="salary-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th style={{ textAlign: 'right' }}>Basic</th>
                                <th style={{ textAlign: 'right' }}>HRA</th>
                                <th style={{ textAlign: 'right' }}>Allowances</th>
                                <th style={{ textAlign: 'right' }}>PF</th>
                                <th style={{ textAlign: 'right' }}>ESI</th>
                                <th style={{ textAlign: 'right' }}>Gross</th>
                                <th style={{ textAlign: 'right' }}>Net Salary</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {salaryRecords.map((record) => {
                                const employee = employees.find(e => e.id === record.employee_id);
                                return (
                                    <tr key={record.id}>
                                        <td>
                                            <div className="employee-info">
                                                <div className="employee-avatar">
                                                    {employee?.name.charAt(0) || '?'}
                                                </div>
                                                <div>
                                                    <div className="employee-name">{employee?.name}</div>
                                                    <div className="employee-code">{employee?.employee_code}</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="amount-cell">{formatCurrency(record.basic_salary)}</td>
                                        <td className="amount-cell earnings">{formatCurrency(record.hra)}</td>
                                        <td className="amount-cell earnings">{formatCurrency(record.allowances)}</td>
                                        <td className="amount-cell deductions">-{formatCurrency(record.pf_deduction)}</td>
                                        <td className="amount-cell deductions">-{formatCurrency(record.esi_deduction)}</td>
                                        <td className="amount-cell">{formatCurrency(record.gross_salary)}</td>
                                        <td className="amount-cell net">{formatCurrency(record.net_salary)}</td>
                                        <td>
                                            <span className={`status-badge ${record.is_paid ? 'paid' : 'pending'}`}>
                                                {record.is_paid ? 'Paid' : 'Pending'}
                                            </span>
                                        </td>
                                        <td>
                                            <button className="action-btn">📄 Slip</button>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
}
