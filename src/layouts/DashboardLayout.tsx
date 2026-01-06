import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

export default function DashboardLayout() {
    return (
        <div className="flex h-screen w-full bg-slate-50 dark:bg-slate-900">
            <Sidebar />
            <div className="flex flex-1 flex-col h-full overflow-hidden">
                <Header />
                <main className="flex-1 overflow-y-auto p-6 bg-slate-50 dark:bg-slate-900">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}

