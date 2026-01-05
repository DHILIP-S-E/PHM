import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
    baseURL: '/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor - add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor - handle errors
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        // Handle 401 - token expired
        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;

            try {
                const refreshToken = localStorage.getItem('refresh_token');
                if (refreshToken) {
                    const response = await axios.post('/api/v1/auth/refresh-token', {
                        refresh_token: refreshToken,
                    });

                    const { access_token } = response.data;
                    localStorage.setItem('access_token', access_token);

                    originalRequest.headers.Authorization = `Bearer ${access_token}`;
                    return api(originalRequest);
                }
            } catch (refreshError) {
                // Refresh failed - logout user
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '/login';
            }
        }

        return Promise.reject(error);
    }
);

export default api;

// Auth API
export const authApi = {
    login: (email: string, password: string) =>
        api.post('/auth/login', { email, password }),

    logout: () => api.post('/auth/logout'),

    refreshToken: (refreshToken: string) =>
        api.post('/auth/refresh-token', { refresh_token: refreshToken }),
};

// Users API
export const usersApi = {
    list: (params?: { page?: number; size?: number; search?: string }) =>
        api.get('/users', { params }),

    get: (id: string) => api.get(`/users/${id}`),

    create: (data: any) => api.post('/users', data),

    update: (id: string, data: any) => api.put(`/users/${id}`, data),

    delete: (id: string) => api.delete(`/users/${id}`),
};

// Warehouses API
export const warehousesApi = {
    list: (params?: { page?: number; size?: number; search?: string; status?: string }) =>
        api.get('/warehouses', { params }),

    get: (id: string) => api.get(`/warehouses/${id}`),

    create: (data: any) => api.post('/warehouses', data),

    update: (id: string, data: any) => api.put(`/warehouses/${id}`, data),

    delete: (id: string) => api.delete(`/warehouses/${id}`),

    getShops: (id: string) => api.get(`/warehouses/${id}/shops`),

    getStock: (id: string, params?: { page?: number; size?: number }) =>
        api.get(`/warehouses/${id}/stock`, { params }),
};

// Shops API
export const shopsApi = {
    list: (params?: { page?: number; size?: number; search?: string; status?: string; warehouse_id?: string }) =>
        api.get('/shops', { params }),

    get: (id: string) => api.get(`/shops/${id}`),

    create: (data: any) => api.post('/shops', data),

    update: (id: string, data: any) => api.put(`/shops/${id}`, data),

    delete: (id: string) => api.delete(`/shops/${id}`),

    getStock: (id: string, params?: { page?: number; size?: number; low_stock?: boolean }) =>
        api.get(`/shops/${id}/stock`, { params }),
};

// Medicines API
export const medicinesApi = {
    list: (params?: { page?: number; size?: number; search?: string; category?: string; manufacturer?: string }) =>
        api.get('/medicines', { params }),

    get: (id: string) => api.get(`/medicines/${id}`),

    create: (data: any) => api.post('/medicines', data),

    update: (id: string, data: any) => api.put(`/medicines/${id}`, data),

    delete: (id: string) => api.delete(`/medicines/${id}`),

    getBatches: (id: string) => api.get(`/medicines/${id}/batches`),

    createBatch: (id: string, data: any) => api.post(`/medicines/${id}/batches`, data),
};

// Inventory API
export const inventoryApi = {
    getMovements: (params?: { page?: number; size?: number; location_type?: string; location_id?: string; movement_type?: string }) =>
        api.get('/stock/movements', { params }),

    adjustStock: (data: any) => api.post('/stock/adjust', data),

    getAlerts: (alertType?: string) =>
        api.get('/stock/alerts', { params: { alert_type: alertType } }),
};

// Purchase Requests API
export const purchaseRequestsApi = {
    list: (params?: { page?: number; size?: number; status?: string; shop_id?: string; warehouse_id?: string }) =>
        api.get('/purchase-requests', { params }),

    get: (id: string) => api.get(`/purchase-requests/${id}`),

    create: (data: any) => api.post('/purchase-requests', data),

    approve: (id: string, data: any) => api.put(`/purchase-requests/${id}/approve`, data),

    reject: (id: string) => api.put(`/purchase-requests/${id}/reject`),
};

// Dispatches API
export const dispatchesApi = {
    list: (params?: { page?: number; size?: number; status?: string; warehouse_id?: string; shop_id?: string }) =>
        api.get('/dispatches', { params }),

    get: (id: string) => api.get(`/dispatches/${id}`),

    create: (data: any) => api.post('/dispatches', data),

    updateStatus: (id: string, data: any) => api.put(`/dispatches/${id}/status`, data),
};

// Invoices API
export const invoicesApi = {
    list: (params?: { page?: number; size?: number; shop_id?: string; customer_id?: string; status?: string }) =>
        api.get('/invoices', { params }),

    get: (id: string) => api.get(`/invoices/${id}`),

    create: (data: any) => api.post('/invoices', data),

    getItems: (id: string) => api.get(`/invoices/${id}/items`),

    processReturn: (id: string, data: any) => api.post(`/invoices/${id}/returns`, data),
};

// Customers API
export const customersApi = {
    list: (params?: { page?: number; size?: number; search?: string; shop_id?: string }) =>
        api.get('/customers', { params }),

    get: (id: string) => api.get(`/customers/${id}`),

    create: (data: any) => api.post('/customers', data),

    update: (id: string, data: any) => api.put(`/customers/${id}`, data),

    getFollowups: (id: string) => api.get(`/customers/${id}/followups`),

    createFollowup: (id: string, data: any) => api.post(`/customers/${id}/followups`, data),
};

// Employees API
export const employeesApi = {
    list: (params?: { page?: number; size?: number; search?: string; department?: string; shop_id?: string }) =>
        api.get('/employees', { params }),

    get: (id: string) => api.get(`/employees/${id}`),

    create: (data: any) => api.post('/employees', data),

    update: (id: string, data: any) => api.put(`/employees/${id}`, data),

    markAttendance: (data: any) => api.post('/employees/attendance', data),

    getAttendance: (id: string, params?: { month?: number; year?: number }) =>
        api.get(`/employees/attendance/${id}`, { params }),

    processSalary: (data: any) => api.post('/employees/salary/process', data),
};

// Reports API
export const reportsApi = {
    getSales: (params?: { shop_id?: string; date_from?: string; date_to?: string }) =>
        api.get('/reports/sales', { params }),

    getDailySales: (params?: { shop_id?: string; date?: string }) =>
        api.get('/reports/sales/daily', { params }),

    getMonthlySales: (params?: { shop_id?: string; month?: number; year?: number }) =>
        api.get('/reports/sales/monthly', { params }),

    getInventory: (params?: { warehouse_id?: string; shop_id?: string }) =>
        api.get('/reports/inventory', { params }),

    getProfitLoss: (params?: { shop_id?: string; month?: number; year?: number }) =>
        api.get('/reports/profit-loss', { params }),

    getExpiry: (params?: { warehouse_id?: string; shop_id?: string; days_ahead?: number }) =>
        api.get('/reports/expiry', { params }),
};

// Notifications API
export const notificationsApi = {
    list: (params?: { page?: number; size?: number; is_read?: boolean; notification_type?: string }) =>
        api.get('/notifications', { params }),

    markRead: (id: string) => api.put(`/notifications/${id}/read`),

    markAllRead: () => api.put('/notifications/read-all'),

    delete: (id: string) => api.delete(`/notifications/${id}`),
};

// Settings API
export const settingsApi = {
    get: () => api.get('/settings'),

    update: (data: any) => api.put('/settings', data),

    getTax: () => api.get('/settings/tax'),

    updateTax: (data: any) => api.put('/settings/tax', data),

    getTaxSummary: (params?: { month?: number; year?: number }) =>
        api.get('/settings/tax/summary', { params }),

    getGstReport: (params?: { month?: number; year?: number }) =>
        api.get('/settings/tax/gst', { params }),
};
