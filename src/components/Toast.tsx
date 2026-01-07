import { useState, useEffect } from 'react';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

interface Toast {
    id: string;
    message: string;
    type: ToastType;
}

let toastCount = 0;
const listeners = new Set<(toasts: Toast[]) => void>();
let toasts: Toast[] = [];

const notify = (toasts: Toast[]) => {
    listeners.forEach(listener => listener(toasts));
};

export const toast = {
    success: (message: string) => {
        const newToast: Toast = { id: `toast-${toastCount++}`, message, type: 'success' };
        toasts = [...toasts, newToast];
        notify(toasts);
        setTimeout(() => toast.dismiss(newToast.id), 5000);
    },
    error: (message: string) => {
        const newToast: Toast = { id: `toast-${toastCount++}`, message, type: 'error' };
        toasts = [...toasts, newToast];
        notify(toasts);
        setTimeout(() => toast.dismiss(newToast.id), 5000);
    },
    warning: (message: string) => {
        const newToast: Toast = { id: `toast-${toastCount++}`, message, type: 'warning' };
        toasts = [...toasts, newToast];
        notify(toasts);
        setTimeout(() => toast.dismiss(newToast.id), 5000);
    },
    info: (message: string) => {
        const newToast: Toast = { id: `toast-${toastCount++}`, message, type: 'info' };
        toasts = [...toasts, newToast];
        notify(toasts);
        setTimeout(() => toast.dismiss(newToast.id), 5000);
    },
    dismiss: (id: string) => {
        toasts = toasts.filter(t => t.id !== id);
        notify(toasts);
    },
};

export function useToast() {
    const [currentToasts, setCurrentToasts] = useState<Toast[]>([]);

    useEffect(() => {
        const listener = (newToasts: Toast[]) => setCurrentToasts(newToasts);
        listeners.add(listener);
        return () => {
            listeners.delete(listener);
        };
    }, []);

    return currentToasts;
}

export default function ToastContainer() {
    const toasts = useToast();

    const getToastIcon = (type: ToastType) => {
        switch (type) {
            case 'success':
                return 'check_circle';
            case 'error':
                return 'error';
            case 'warning':
                return 'warning';
            case 'info':
                return 'info';
        }
    };

    const getToastColor = (type: ToastType) => {
        switch (type) {
            case 'success':
                return 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-800 dark:text-green-200';
            case 'error':
                return 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-800 dark:text-red-200';
            case 'warning':
                return 'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800 text-yellow-800 dark:text-yellow-200';
            case 'info':
                return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800 text-blue-800 dark:text-blue-200';
        }
    };

    return (
        <div className="fixed top-4 right-4 z-[9999] flex flex-col gap-2 max-w-md">
            {toasts.map((toast, index) => (
                <div
                    key={toast.id}
                    className={`flex items-start gap-3 px-4 py-3 rounded-lg border shadow-lg backdrop-blur-sm animate-slideInRight ${getToastColor(toast.type)}`}
                    style={{ animationDelay: `${index * 50}ms` }}
                >
                    <span className="material-symbols-outlined text-[20px] mt-0.5">
                        {getToastIcon(toast.type)}
                    </span>
                    <p className="flex-1 text-sm font-medium">{toast.message}</p>
                    <button
                        onClick={() => window.toast?.dismiss(toast.id)}
                        className="text-current opacity-60 hover:opacity-100 transition-opacity"
                    >
                        <span className="material-symbols-outlined text-[18px]">close</span>
                    </button>
                </div>
            ))}
        </div>
    );
}

// Make toast globally available
declare global {
    interface Window {
        toast: typeof toast;
    }
}

if (typeof window !== 'undefined') {
    window.toast = toast;
}
