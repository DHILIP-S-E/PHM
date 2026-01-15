interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'ghost' | 'danger' | 'outline';
    children: React.ReactNode;
    icon?: string;
    loading?: boolean;
}

export default function Button({
    variant = 'primary',
    children,
    icon,
    loading,
    className = '',
    disabled,
    ...props
}: ButtonProps) {
    const baseClass = 'btn';

    // Map variants to classes (assuming Tailwind integration or use utility classes directly)
    // Since we don't see the CSS file, we'll append utility classes for specific new variants if expected,
    // or rely on the class name generation convention if it exists. 
    // However, looking at the previous file, it used 'btn-primary' and 'btn-secondary'.
    // We should probably define these or add inline styles/utility classes for the new ones.
    // Given the context of Tailwind, let's map them to utility classes if standard classes don't exist.

    let variantClass = '';
    switch (variant) {
        case 'primary': variantClass = 'btn-primary'; break;
        case 'secondary': variantClass = 'btn-secondary'; break;
        case 'ghost': variantClass = 'bg-transparent hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 border-transparent shadow-none'; break;
        case 'danger': variantClass = 'bg-red-50 text-red-600 hover:bg-red-100 border-red-200 shadow-sm'; break;
        case 'outline': variantClass = 'bg-transparent border border-slate-300 text-slate-700 hover:bg-slate-50'; break;
        default: variantClass = 'btn-primary';
    }

    return (
        <button
            className={`${baseClass} ${variantClass} ${className} flex items-center justify-center gap-2 transition-all font-medium rounded-lg disabled:opacity-50 disabled:cursor-not-allowed`}
            disabled={disabled || loading}
            {...props}
        >
            {loading ? (
                <span className="animate-spin rounded-full h-4 w-4 border-2 border-current border-t-transparent"></span>
            ) : icon ? (
                <span className="material-symbols-outlined text-[20px]">{icon}</span>
            ) : null}
            {children}
        </button>
    );
}
