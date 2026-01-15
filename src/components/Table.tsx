export interface Column<T> {
    key: keyof T | string;
    header: string;
    render?: (item: T) => React.ReactNode;
    align?: 'left' | 'right' | 'center';
    className?: string;
    numeric?: boolean; // Enterprise: auto right-align numeric columns
}

interface TableProps<T> {
    data: T[];
    columns: Column<T>[];
    loading?: boolean;
    emptyMessage?: string;
    zebra?: boolean; // Enterprise: zebra striping option
}

export interface Column<T> {
    key: keyof T | string;
    header: string;
    render?: (item: T) => React.ReactNode;
    align?: 'left' | 'right' | 'center';
    className?: string;
    numeric?: boolean;
    width?: string;
}

interface PaginationProps {
    currentPage: number;
    totalPages: number;
    totalItems: number;
    pageSize: number;
    onPageChange: (page: number) => void;
}

interface TableProps<T> {
    data: T[];
    columns: Column<T>[];
    loading?: boolean;
    emptyMessage?: string;
    zebra?: boolean;
    stickyHeader?: boolean;
    pagination?: PaginationProps;
    error?: string;
    onRetry?: () => void;
    headerSlot?: React.ReactNode;
}

export default function Table<T extends Record<string, any>>({
    data,
    columns,
    loading = false,
    emptyMessage = 'No data available',
    zebra = false,
    stickyHeader = true,
    pagination,
    error,
    onRetry,
    headerSlot
}: TableProps<T>) {

    // Helper to render skeleton rows
    const renderSkeletons = () => {
        return Array(5).fill(0).map((_, idx) => (
            <tr key={`skel-${idx}`} className="animate-pulse border-b border-slate-100 dark:border-slate-800">
                {columns.map((_, colIdx) => (
                    <td key={colIdx} className="px-4 py-4">
                        <div className="h-4 bg-slate-200 dark:bg-slate-700 rounded w-3/4"></div>
                    </td>
                ))}
            </tr>
        ));
    };

    if (error) {
        return (
            <div className="flex flex-col items-center justify-center py-16 text-center text-slate-500 bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700">
                <div className="w-12 h-12 rounded-full bg-red-50 dark:bg-red-900/20 flex items-center justify-center mb-3">
                    <span className="material-symbols-outlined text-red-500 text-[24px]">error</span>
                </div>
                <h3 className="text-lg font-medium text-slate-900 dark:text-white">Failed to load data</h3>
                <p className="text-sm mt-1 mb-4 max-w-xs">{error}</p>
                {onRetry && (
                    <button
                        onClick={onRetry}
                        className="px-4 py-2 bg-white border border-slate-300 rounded-lg text-sm font-medium hover:bg-slate-50 transition-colors"
                    >
                        Try Again
                    </button>
                )}
            </div>
        );
    }

    return (
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-sm border border-slate-200 dark:border-slate-700 overflow-hidden flex flex-col h-full">
            {/* Embedded Header Slot (e.g., List Filters) */}
            {headerSlot && (
                <div className="border-b border-slate-100 dark:border-slate-700">
                    {headerSlot}
                </div>
            )}

            <div className="overflow-x-auto flex-1 relative">
                <table className={`w-full text-left text-sm ${zebra ? 'table-zebra' : ''} border-collapse`}>
                    <thead className={`bg-slate-50 dark:bg-slate-900/90 z-10 ${stickyHeader ? 'sticky top-0' : ''}`}>
                        <tr>
                            {columns.map((column, index) => {
                                const alignClass = column.numeric ? 'text-right' :
                                    column.align === 'right' ? 'text-right' :
                                        column.align === 'center' ? 'text-center' : 'text-left';
                                return (
                                    <th
                                        key={index}
                                        className={`px-4 py-3 font-semibold text-slate-900 dark:text-white uppercase text-xs tracking-wider ${alignClass} ${column.className || ''}`}
                                        style={{ width: column.width }}
                                    >
                                        {column.header}
                                    </th>
                                );
                            })}
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 dark:divide-slate-700 bg-white dark:bg-slate-800">
                        {loading ? (
                            renderSkeletons()
                        ) : data.length === 0 ? (
                            <tr>
                                <td colSpan={columns.length} className="px-4 py-16 text-center text-slate-500">
                                    <div className="flex flex-col items-center gap-3">
                                        <div className="w-12 h-12 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center">
                                            <span className="material-symbols-outlined text-slate-400">inbox</span>
                                        </div>
                                        <p className="font-medium text-slate-600 dark:text-slate-400">{emptyMessage}</p>
                                    </div>
                                </td>
                            </tr>
                        ) : (
                            data.map((item, rowIndex) => (
                                <tr key={rowIndex} className="hover:bg-slate-50 dark:hover:bg-slate-700/50 transition-colors group">
                                    {columns.map((column, colIndex) => {
                                        const value = column.render
                                            ? column.render(item)
                                            : item[column.key as keyof T];
                                        const alignClass = column.numeric ? 'text-right' :
                                            column.align === 'right' ? 'text-right' :
                                                column.align === 'center' ? 'text-center' : 'text-left';

                                        return (
                                            <td
                                                key={colIndex}
                                                className={`px-4 py-3 text-slate-600 dark:text-slate-300 ${alignClass} ${column.className || ''}`}
                                            >
                                                {value}
                                            </td>
                                        );
                                    })}
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>

            {/* Pagination Footer */}
            {pagination && !loading && !error && data.length > 0 && (
                <div className="border-t border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-900/50 px-4 py-3 flex items-center justify-between">
                    <div className="text-sm text-slate-500 dark:text-slate-400">
                        Showing <span className="font-medium">{(pagination.currentPage - 1) * pagination.pageSize + 1}</span> to <span className="font-medium">{Math.min(pagination.currentPage * pagination.pageSize, pagination.totalItems)}</span> of <span className="font-medium">{pagination.totalItems}</span>
                    </div>
                    <div className="flex gap-2">
                        <button
                            onClick={() => pagination.onPageChange(Math.max(1, pagination.currentPage - 1))}
                            disabled={pagination.currentPage === 1}
                            className="p-1.5 rounded-lg hover:bg-white dark:hover:bg-slate-800 border border-transparent hover:border-slate-200 dark:hover:border-slate-700 disabled:opacity-30 disabled:hover:bg-transparent transition-all"
                            title="Previous Page"
                        >
                            <span className="material-symbols-outlined text-[20px]">chevron_left</span>
                        </button>
                        <button
                            onClick={() => pagination.onPageChange(Math.min(pagination.totalPages, pagination.currentPage + 1))}
                            disabled={pagination.currentPage === pagination.totalPages}
                            className="p-1.5 rounded-lg hover:bg-white dark:hover:bg-slate-800 border border-transparent hover:border-slate-200 dark:hover:border-slate-700 disabled:opacity-30 disabled:hover:bg-transparent transition-all"
                            title="Next Page"
                        >
                            <span className="material-symbols-outlined text-[20px]">chevron_right</span>
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
