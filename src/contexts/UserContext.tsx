import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import { authApi } from '../services/api';

export interface User {
    id: string;
    email: string;
    full_name: string;
    phone?: string;
    role: string;
    is_active: boolean;
    last_login?: string;
    created_at?: string;
}

interface UserContextType {
    user: User | null;
    loading: boolean;
    error: string | null;
    refreshUser: () => Promise<void>;
}

const UserContext = createContext<UserContextType>({
    user: null,
    loading: true,
    error: null,
    refreshUser: async () => { },
});

export const useUser = () => useContext(UserContext);

interface UserProviderProps {
    children: ReactNode;
}

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchUser = async () => {
        try {
            setLoading(true);
            setError(null);

            const token = localStorage.getItem('access_token');
            console.log('🔐 UserContext: Has token?', !!token, token?.substring(0, 20) + '...');

            if (!token) {
                setUser(null);
                setLoading(false);
                return;
            }

            const response = await authApi.me();
            console.log('✅ UserContext: API Response:', response.data);
            setUser(response.data);

            // Store user name in localStorage for quick access
            localStorage.setItem('user_name', response.data.full_name);
            localStorage.setItem('user_role', response.data.role);
        } catch (err: any) {
            console.error('❌ UserContext ERROR:', err);
            console.error('❌ Status:', err.response?.status);
            console.error('❌ Data:', err.response?.data);
            setError(err.message || 'Failed to load user data');

            // Clear invalid tokens
            if (err.response?.status === 401) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                localStorage.removeItem('user_name');
                localStorage.removeItem('user_role');
                setUser(null);
            }
        } finally {
            setLoading(false);
        }
    };

    const refreshUser = async () => {
        await fetchUser();
    };

    useEffect(() => {
        fetchUser();
    }, []);

    return (
        <UserContext.Provider value={{ user, loading, error, refreshUser }}>
            {children}
        </UserContext.Provider>
    );
};
