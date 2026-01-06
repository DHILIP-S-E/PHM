import { useState, useEffect } from 'react';
import { employeesApi } from '../services/api';

interface Employee {
    id: string;
    employee_code: string;
    name: string;
    designation: string;
    department: string;
}

interface AttendanceRecord {
    employee_id: string;
    date: string;
    status: 'present' | 'absent' | 'half_day' | 'leave';
    check_in?: string;
    check_out?: string;
}

export default function AttendanceManagement() {
    const [employees, setEmployees] = useState<Employee[]>([]);
    const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
    const [attendance, setAttendance] = useState<Record<string, AttendanceRecord>>({});
    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [message, setMessage] = useState({ type: '', text: '' });
    const [viewMode, setViewMode] = useState<'mark' | 'summary'>('mark');


    useEffect(() => {
        loadEmployees();
    }, []);

    useEffect(() => {
        if (viewMode === 'mark') {
            loadAttendanceForDate();
        }
    }, [selectedDate, employees]);

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

    const loadAttendanceForDate = async () => {
        // Initialize attendance state for all employees
        const initialAttendance: Record<string, AttendanceRecord> = {};
        employees.forEach(emp => {
            initialAttendance[emp.id] = {
                employee_id: emp.id,
                date: selectedDate,
                status: 'present',
                check_in: '09:00',
                check_out: '18:00'
            };
        });
        setAttendance(initialAttendance);
    };

    const updateAttendance = (employeeId: string, field: string, value: string) => {
        setAttendance(prev => ({
            ...prev,
            [employeeId]: {
                ...prev[employeeId],
                [field]: value
            }
        }));
    };

    const submitAttendance = async () => {
        setSubmitting(true);
        try {
            const records = Object.values(attendance);
            for (const record of records) {
                await employeesApi.markAttendance(record);
            }
            setMessage({ type: 'success', text: 'Attendance saved successfully!' });
        } catch (error: any) {
            setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to save attendance' });
        } finally {
            setSubmitting(false);
        }
    };

    const getStatusColor = (status: string) => {
        const colors: Record<string, string> = {
            present: '#10b981',
            absent: '#ef4444',
            half_day: '#f59e0b',
            leave: '#8b5cf6'
        };
        return colors[status] || '#666';
    };

    const stats = {
        total: employees.length,
        present: Object.values(attendance).filter(a => a.status === 'present').length,
        absent: Object.values(attendance).filter(a => a.status === 'absent').length,
        half_day: Object.values(attendance).filter(a => a.status === 'half_day').length,
        leave: Object.values(attendance).filter(a => a.status === 'leave').length
    };

    return (
        <div className="attendance-management">
            <style>{`
                .attendance-management {
                    padding: 24px;
                    max-width: 1200px;
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
                .view-toggle {
                    display: flex;
                    gap: 8px;
                }
                .toggle-btn {
                    padding: 10px 20px;
                    border: 1px solid #ddd;
                    background: white;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: 500;
                }
                .toggle-btn.active {
                    background: #4a6cf7;
                    color: white;
                    border-color: #4a6cf7;
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
                .date-picker {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }
                .date-picker label {
                    font-weight: 500;
                    color: #333;
                }
                .date-picker input {
                    padding: 10px 16px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    font-size: 15px;
                }
                .stats-row {
                    display: flex;
                    gap: 24px;
                }
                .stat-item {
                    text-align: center;
                }
                .stat-value {
                    font-size: 24px;
                    font-weight: 700;
                }
                .stat-label {
                    font-size: 12px;
                    color: #666;
                    text-transform: uppercase;
                }
                .attendance-table {
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
                    padding: 14px 16px;
                    text-align: left;
                    border-bottom: 1px solid #eee;
                }
                th {
                    background: #f8f9ff;
                    font-weight: 600;
                    color: #333;
                    font-size: 13px;
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
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    background: linear-gradient(135deg, #4a6cf7, #6366f1);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: 600;
                }
                .employee-name {
                    font-weight: 500;
                    color: #333;
                }
                .employee-code {
                    font-size: 12px;
                    color: #888;
                }
                .status-select {
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    font-size: 14px;
                    cursor: pointer;
                    min-width: 120px;
                }
                .time-input {
                    padding: 8px 12px;
                    border: 1px solid #ddd;
                    border-radius: 6px;
                    font-size: 14px;
                    width: 100px;
                }
                .btn-submit {
                    padding: 12px 32px;
                    background: linear-gradient(135deg, #4a6cf7, #6366f1);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: transform 0.2s;
                }
                .btn-submit:hover {
                    transform: translateY(-2px);
                }
                .btn-submit:disabled {
                    opacity: 0.6;
                    cursor: not-allowed;
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
                .table-footer {
                    padding: 16px;
                    display: flex;
                    justify-content: flex-end;
                    background: #f8f9ff;
                }
                .loading {
                    text-align: center;
                    padding: 60px;
                    color: #666;
                }
            `}</style>

            <div className="page-header">
                <h1>📋 Attendance Management</h1>
                <div className="view-toggle">
                    <button
                        className={`toggle-btn ${viewMode === 'mark' ? 'active' : ''}`}
                        onClick={() => setViewMode('mark')}
                    >
                        Mark Attendance
                    </button>
                    <button
                        className={`toggle-btn ${viewMode === 'summary' ? 'active' : ''}`}
                        onClick={() => setViewMode('summary')}
                    >
                        Summary
                    </button>
                </div>
            </div>

            {message.text && (
                <div className={`message ${message.type}`}>
                    {message.text}
                </div>
            )}

            <div className="controls-card">
                <div className="date-picker">
                    <label>Date:</label>
                    <input
                        type="date"
                        value={selectedDate}
                        onChange={(e) => setSelectedDate(e.target.value)}
                    />
                </div>
                <div className="stats-row">
                    <div className="stat-item">
                        <div className="stat-value" style={{ color: '#10b981' }}>{stats.present}</div>
                        <div className="stat-label">Present</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value" style={{ color: '#ef4444' }}>{stats.absent}</div>
                        <div className="stat-label">Absent</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value" style={{ color: '#f59e0b' }}>{stats.half_day}</div>
                        <div className="stat-label">Half Day</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-value" style={{ color: '#8b5cf6' }}>{stats.leave}</div>
                        <div className="stat-label">Leave</div>
                    </div>
                </div>
            </div>

            {loading ? (
                <div className="loading">Loading employees...</div>
            ) : (
                <div className="attendance-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Department</th>
                                <th>Status</th>
                                <th>Check In</th>
                                <th>Check Out</th>
                            </tr>
                        </thead>
                        <tbody>
                            {employees.map(employee => (
                                <tr key={employee.id}>
                                    <td>
                                        <div className="employee-info">
                                            <div className="employee-avatar">
                                                {employee.name.charAt(0)}
                                            </div>
                                            <div>
                                                <div className="employee-name">{employee.name}</div>
                                                <div className="employee-code">{employee.employee_code}</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td>{employee.department}</td>
                                    <td>
                                        <select
                                            className="status-select"
                                            value={attendance[employee.id]?.status || 'present'}
                                            onChange={(e) => updateAttendance(employee.id, 'status', e.target.value)}
                                            style={{ borderColor: getStatusColor(attendance[employee.id]?.status || 'present') }}
                                        >
                                            <option value="present">Present</option>
                                            <option value="absent">Absent</option>
                                            <option value="half_day">Half Day</option>
                                            <option value="leave">Leave</option>
                                        </select>
                                    </td>
                                    <td>
                                        <input
                                            type="time"
                                            className="time-input"
                                            value={attendance[employee.id]?.check_in || '09:00'}
                                            onChange={(e) => updateAttendance(employee.id, 'check_in', e.target.value)}
                                            disabled={attendance[employee.id]?.status === 'absent' || attendance[employee.id]?.status === 'leave'}
                                        />
                                    </td>
                                    <td>
                                        <input
                                            type="time"
                                            className="time-input"
                                            value={attendance[employee.id]?.check_out || '18:00'}
                                            onChange={(e) => updateAttendance(employee.id, 'check_out', e.target.value)}
                                            disabled={attendance[employee.id]?.status === 'absent' || attendance[employee.id]?.status === 'leave'}
                                        />
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                    <div className="table-footer">
                        <button
                            className="btn-submit"
                            onClick={submitAttendance}
                            disabled={submitting}
                        >
                            {submitting ? 'Saving...' : 'Save Attendance'}
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
