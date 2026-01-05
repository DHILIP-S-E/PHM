import { Outlet } from 'react-router-dom';
import Sidebar from '../components/Sidebar';
import Header from '../components/Header';

export default function DashboardLayout() {
    return (
        <div className="flex h-screen w-full bg-background-light dark:bg-background-dark">
            <Sidebar />
            <div className="flex flex-1 flex-col h-full overflow-hidden">
                <Header />
                <main className="flex-1 overflow-y-auto bg-background-light dark:bg-background-dark">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}
