import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../contexts/UserContext';
import { getRoleName } from '../utils/rbac';

export default function Header() {
    const [searchQuery, setSearchQuery] = useState('');
    const [darkMode, setDarkMode] = useState(() => {
        if (typeof window !== 'undefined') {
            return document.documentElement.classList.contains('dark');
        }
        return false;
    });
    const [showUserMenu, setShowUserMenu] = useState(false);
    const navigate = useNavigate();
    const { user } = useUser();

    // Default fallback user data
    const userName = user?.full_name || 'User';
    const userEmail = user?.email || 'user@example.com';
    const userRole = getRoleName(user?.role || 'user');
    const userInitials = userName.split(' ').map((n: string) => n[0]).join('').toUpperCase().substring(0, 2);

    useEffect(() => {
        if (darkMode) {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }, [darkMode]);

    const toggleTheme = () => {
        setDarkMode(!darkMode);
    };

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigate('/login');
    };



    return (
        <header className="flex h-14 items-center justify-end border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-6 sticky top-0 z-10">
            {/* Right: Actions */}
            <div className="flex items-center gap-2">
                {/* Theme Toggle */}
                <button
                    onClick={toggleTheme}
                    className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-primary hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
                    title={darkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
                >
                    <span className="material-symbols-outlined text-[20px]">
                        {darkMode ? 'light_mode' : 'dark_mode'}
                    </span>
                </button>

                {/* Notifications */}
                <button
                    onClick={() => navigate('/notifications')}
                    className="relative flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:text-primary hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
                    title="Notifications"
                >
                    <span className="material-symbols-outlined text-[20px]">notifications</span>
                    <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-red-500"></span>
                </button>


            </div>
        </header>
    );
}

