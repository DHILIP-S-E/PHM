import { NavLink, useLocation } from 'react-router-dom';

const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: 'dashboard' },
    { path: '/warehouses', label: 'Warehouses', icon: 'warehouse' },
    { path: '/shops', label: 'Medical Shops', icon: 'storefront' },
    { path: '/medicines', label: 'Medicines', icon: 'medication' },
    { path: '/inventory', label: 'Inventory', icon: 'inventory_2' },
    { path: '/invoices', label: 'Sales / POS', icon: 'point_of_sale' },
    { path: '/reports/expiry', label: 'Reports', icon: 'bar_chart' },
    { path: '/employees', label: 'HR', icon: 'badge' },
];

const settingsItems = [
    { path: '/settings/application', label: 'App Settings', icon: 'settings' },
    { path: '/settings/system', label: 'System', icon: 'tune' },
];

export default function Sidebar() {
    const location = useLocation();

    return (
        <aside className="flex w-64 flex-col border-r border-slate-200 dark:border-slate-800 bg-surface-light dark:bg-surface-dark transition-colors duration-300">
            {/* Logo */}
            <div className="flex items-center gap-3 px-6 py-5 border-b border-slate-100 dark:border-slate-800/50">
                <div className="flex items-center justify-center size-10 rounded-xl bg-primary/10 text-primary">
                    <span className="material-symbols-outlined">local_pharmacy</span>
                </div>
                <div>
                    <h1 className="text-lg font-bold tracking-tight text-slate-900 dark:text-white">PharmaEC</h1>
                    <p className="text-xs text-slate-500">Management System</p>
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex flex-1 flex-col gap-1 px-3 py-4 overflow-y-auto">
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group ${isActive
                                ? 'bg-primary text-white'
                                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                            }`
                        }
                    >
                        <span className="material-symbols-outlined">{item.icon}</span>
                        <span className="text-sm font-medium">{item.label}</span>
                    </NavLink>
                ))}

                <div className="my-3 h-px bg-slate-200 dark:bg-slate-700"></div>
                <p className="px-3 text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">Settings</p>

                {settingsItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all group ${isActive
                                ? 'bg-primary/10 text-primary'
                                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                            }`
                        }
                    >
                        <span className="material-symbols-outlined">{item.icon}</span>
                        <span className="text-sm font-medium">{item.label}</span>
                    </NavLink>
                ))}
            </nav>

            {/* Bottom Actions */}
            <div className="p-4 border-t border-slate-200 dark:border-slate-800">
                <button className="flex w-full items-center gap-3 px-3 py-2 text-slate-600 dark:text-slate-400 hover:text-red-500 dark:hover:text-red-400 transition-colors rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800">
                    <span className="material-symbols-outlined">logout</span>
                    <span className="text-sm font-medium">Sign Out</span>
                </button>
            </div>
        </aside>
    );
}
