export type ToastType = 'success' | 'error' | 'warning';

export interface Toast {
    id: string;
    message: string;
    type: ToastType;
}

class ToastManager {
    toasts = $state<Toast[]>([]);

    add = (message: string, type: ToastType = 'success') => {
        const id = crypto.randomUUID();
        this.toasts.push({ id, message, type });

        setTimeout(() => {
            this.remove(id)
        }, 4000);
    };

    remove = (id: string) => {
        this.toasts = this.toasts.filter(t => t.id !== id);
    }
}

export const toaster = new ToastManager();