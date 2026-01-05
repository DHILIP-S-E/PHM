interface StatCardProps {
    title: string;
    value: string | number;
    change?: string;
    changeType?: 'up' | 'down' | 'neutral';
    icon: string;
}

export default function StatCard({ title, value, change, changeType = 'up', icon }: StatCardProps) {
    const changeColors = {
        up: 'text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-500/10',
        down: 'text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-500/10',
        neutral: 'text-slate-600 dark:text-slate-400 bg-slate-50 dark:bg-slate-500/10',
    };

    const changeIcons = {
        up: 'trending_up',
        down: 'trending_down',
        neutral: 'trending_flat',
    };

    return (
        <div className="flex flex-col gap-1 rounded-xl border border-slate-200 dark:border-slate-700 bg-surface-light dark:bg-surface-dark p-5 shadow-sm">
            <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400">{title}</p>
                <span className="material-symbols-outlined text-slate-400">{icon}</span>
            </div>
            <div className="flex items-end gap-2 mt-2">
                <p className="text-2xl font-bold text-slate-900 dark:text-white">{value}</p>
                {change && (
                    <span className={`flex items-center text-xs font-medium ${changeColors[changeType]} px-1.5 py-0.5 rounded mb-1`}>
                        <span className="material-symbols-outlined text-[14px] mr-0.5">{changeIcons[changeType]}</span>
                        {change}
                    </span>
                )}
            </div>
        </div>
    );
}
