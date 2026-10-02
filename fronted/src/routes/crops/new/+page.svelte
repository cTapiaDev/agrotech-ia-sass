<script lang="ts">
    import api from "$lib/api";
    import { goto } from "$app/navigation";
    import { toaster } from "$lib/toast.svelte";

    let name = $state('');
    let crop_type = $state('');
    let sowing_date = $state('');
    let harvest_date = $state('');
    let farm_field = $state<number | ''>('');
    let isSubmitting = $state(false);

    const handleSubmit = async (event: Event) => {
        event.preventDefault();
        isSubmitting = true;

        try {
            await api.post('/crops/', {
                name,
                crop_type, 
                sowing_date, 
                harvest_date: harvest_date || null, 
                farm_field_id: farm_field
            });

            toaster.add('Cultivo registrado exitosamente.', 'success');
            goto('/');
        } catch (error) {
            console.error('Fallo al crear el registro:', error);
        } finally {
            isSubmitting = false;
        }
    }
</script>

<main class="min-h-screen bg-slate-50 p-8">
    <div class="mx-auto max-w-xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div class="mb-8 flex items-center justify-between">
            <h2 class="text-2xl font-bold text-slate-900">Nuevo Cultivo</h2>
            <button onclick={() => goto('/')} class="cursor-pointer text-sm font-semibold text-indigo-600 hover:text-indigo-800">
                Volver al panel
            </button>
        </div>

        <form class="flex flex-col gap-6" onsubmit={handleSubmit}>
            <div class="flex flex-col gap-2">
                <label for="name" class="text-sm font-semibold text-slate-700">Nombre del Cultivo</label>
                <input 
                    type="text" 
                    id="name" 
                    bind:value={name}
                    placeholder="Ej. Maíz"
                    required
                    class="rounded-lg border border-slate-300 bg-slate-50 px-4 py-2 outline-none transition-all focus:border-emerald-500 focus:bg-white focus:ring-1 focus:ring-emerald-500"
                >
            </div>

            <div class="flex flex-col gap-2">
                <label for="crop_type" class="text-sm font-semibold text-slate-700">Tipo de Cultivo</label>
                <select
                    id="crop_type"
                    bind:value={crop_type}
                    required
                    class="rounded-lg border border-slate-300 bg-slate-50 px-4 py-2 outline-none transition-all focus:border-emerald-500 focus:bg-white focus:ring-1 focus:ring-emerald-500"
                >
                    <option value="" disabled selected>Selecciona un tipo...</option>
                    <option value="CEREAL">Cereal</option>
                    <option value="FRUIT">Fruta</option>
                    <option value="VEGETABLE">Vegetal</option>
                </select>
            </div>

            <div class="flex flex-col gap-2 mb-4">
                <label for="sowing_date" class="text-sm font-semibold text-slate-700">Fecha de Siembra</label>
                <input 
                    type="date" 
                    id="sowing_date" 
                    bind:value={sowing_date}
                    required
                    class="rounded-lg border border-slate-300 bg-slate-50 px-4 py-2 outline-none transition-all focus:border-emerald-500 focus:bg-white focus:ring-1 focus:ring-emerald-500"
                >
            </div>

            <div class="flex flex-col gap-2 mb-4">
                <label for="harvest_date" class="text-sm font-semibold text-slate-700">Fecha de Cosecha</label>
                <input 
                    type="date" 
                    id="harvest_date" 
                    bind:value={harvest_date}
                    class="rounded-lg border border-slate-300 bg-slate-50 px-4 py-2 outline-none transition-all focus:border-emerald-500 focus:bg-white focus:ring-1 focus:ring-emerald-500"
                >
            </div>

            <div class="flex flex-col gap-2">
                <label for="farm_field" class="text-sm font-semibold text-slate-700">ID del campo</label>
                <input 
                    type="number" 
                    id="farm_field" 
                    bind:value={farm_field}
                    placeholder="ID del campo (Ej. 1)"
                    required
                    min="1"
                    class="rounded-lg border border-slate-300 bg-slate-50 px-4 py-2 outline-none transition-all focus:border-emerald-500 focus:bg-white focus:ring-1 focus:ring-emerald-500"
                >
            </div>

            <button type="submit" disabled={isSubmitting} class="cursor-pointer rounded-lg bg-emerald-600 py-3 font-bold text-white transition-colors hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-emerald-400 shadow-md">
                {isSubmitting ? 'Guardando...' : 'Registrar Cultivo'}
            </button>
        </form>
    </div>
</main>