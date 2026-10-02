<script lang="ts">
    const { data } = $props();
    const crop = data.crop;
</script>

<main class="min-h-screen bg-slate-50 p-8">
    <div class="mx-auto max-w-xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div class="flex items-center justify-between border-b border-slate-200">
            <h2 class="text-xl font-bold text-slate-900">Detalle del Cultivo</h2>
            <a href="/" class="cursor-pointer text-sm font-semibold text-indigo-600 hover:text-indigo-800">Volver al panel</a>
        </div>

        <div class="p-6">
            <div class="grid grid-cols-2 gap-6">
                <div>
                    <span class="block text-xs font-bold uppercase text-slate-500 mb-1">Nombre</span>
                    <span class="block text-lg font-medium text-slate-900">{crop.name}</span>
                </div>
                <div>
                    <span class="block text-xs font-bold uppercase text-slate-500 mb-1">Tipo</span>
                    <span class="inline-block rounded-full bg-emerald-100 px-3 py-1 text-sm text-slate-900">{crop.crop_type}</span>
                </div>
                <div>
                    <span class="block text-xs font-bold uppercase text-slate-500 mb-1">Fecha de Siembra</span>
                    <span class="block font-medium text-slate-800">{crop.sowing_date}</span>
                </div>
                <div>
                    <span class="block text-xs font-bold uppercase text-slate-500 mb-1">Fecha de Cosecha</span>
                    <span class="block font-medium text-slate-800">{crop.harvest_date || 'No definida'}</span>
                </div>
                <div>
                    <span class="block text-xs font-bold uppercase text-slate-500 mb-1">ID Campo Asociada</span>
                    <span class="block font-medium text-slate-800">{crop.farm_field_id || crop.farm_field}</span>
                </div>
                <div>
                    <span class="block text-xs font-bold uppercase text-slate-500 mb-1">Estado</span>
                    <span class="block font-medium text-slate-800">{crop.is_active ? 'Activo' : 'Inactivo'}</span>
                </div>
            </div>
        </div>
    </div>
</main>