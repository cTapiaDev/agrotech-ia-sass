<script lang="ts">
    import { toaster } from "$lib/toast.svelte";
</script>

<div class="fixed top-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
    {#each toaster.toasts as toast (toast.id)}
        <div
            class="pointer-events-auto min-w-75 max-w-md rounded-lg p-4 text-sm font-semibold shadow-xl transition-all"
            class:bg-emerald-600={toast.type === 'success'}
            class:bg-red-600={toast.type === 'error'}
            class:bg-amber-500={toast.type === 'warning'}
            class:text-white={true}
        >
            <div class="flex justify-between items-start gap-4">
                <span>{toast.message}</span>
                <button onclick={() => toaster.remove(toast.id)} class="cursoir-pointer opacity-70 hover:opacity-100">X</button>
            </div>
        </div>
    {/each}
</div>