import React from 'react';
import SearchBar from './SearchBar';
import Button from './Button';

interface ListHeaderBarProps {
    title: string;
    count?: number;
    searchProps?: {
        value: string;
        onChange: (value: string) => void;
        placeholder?: string;
    };
    onFilterClick?: () => void;
    actions?: React.ReactNode;
    className?: string;
    embedded?: boolean;
}

export default function ListHeaderBar({
    title,
    count,
    searchProps,
    onFilterClick,
    actions,
    className = '',
    embedded = false
}: ListHeaderBarProps) {
    const containerClasses = embedded
        ? `bg-white dark:bg-slate-800 px-4 py-3 border-b border-slate-100 dark:border-slate-700 ${className}`
        : `bg-white dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 px-4 py-3 ${className}`;

    return (
        <div className={containerClasses}>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                {/* Left Side: Title & Count */}
                <h2 className="text-base font-semibold text-slate-900 dark:text-white flex items-center gap-2">
                    {title}
                    {count !== undefined && (
                        <span className="px-2 py-0.5 text-xs font-medium bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 rounded-full">
                            {count}
                        </span>
                    )}
                </h2>

                {/* Right Side: Controls */}
                <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap">
                    {searchProps && (
                        <div className="w-full sm:w-auto min-w-[220px]">
                            <SearchBar
                                value={searchProps.value}
                                onChange={searchProps.onChange}
                                placeholder={searchProps.placeholder || "Search..."}
                                className="!w-full"
                            />
                        </div>
                    )}

                    {onFilterClick && (
                        <Button
                            variant="secondary"
                            onClick={onFilterClick}
                            className="!p-2"
                            title="Filter List"
                        >
                            <span className="material-symbols-outlined text-[20px] text-slate-500">filter_list</span>
                        </Button>
                    )}

                    {actions}
                </div>
            </div>
        </div>
    );
}
