<script lang="ts">
    import { env } from '$env/dynamic/public';

    let responseData = $state<any>(null);
    let isLoading = $state<boolean>(false);
    let errorMessage = $state<string | null>(null);

    const fetchCropsData = async () => {
        isLoading = true;
        errorMessage = null;

        try {
            const response = await fetch(`${env.PUBLIC_API_URL}/crops/`);

            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status} - El servidor rechazó la conexión`)
            }

            const data = await response.json();
            responseData = data;
        } catch (error: any) {
            errorMessage = error.message || 'Fallo de red: Verifica que los CORS estén activos.';
            responseData = null;
        } finally {
            isLoading = false;
        }
    }
</script>

<main class="flex min-h-screen flex-col items-center justify-center bg-slate-50 p-6">
    <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight mb-8">Svelte</h1>

    <button 
        class="cursor-pointer rounded-lg bg-indigo-600 px-6 py-3 font-semibold text-white shadow-sm transition-all hover:bg-indigo-700"
        onclick={fetchCropsData}
        disabled={isLoading}
    >
        {isLoading ? 'Conectando...' : 'Obtener Cultivos'}
    </button>

    {#if errorMessage}
        <div class="mt-6 w-full max-w-2xl rounded-md border border-red-300 bg-red-100 p-4 text-red-700">
            {errorMessage}
        </div>
    {/if}

    {#if responseData}
        <div class="mt-6 w-full max-w-2xl overflow-hidden rounded-lg bg-slate-900 shadow-lg">
            <div class="flex items-center justify-between bg-slate-800 px-4 py-2 text-xs font-medium text-white">
                <span>Respuesta GET /api/crops/</span>
            </div>
            <pre class="overflow-x-auto p-4 text-sm font-mono text-emerald-400">{JSON.stringify(responseData, null, 2)}</pre>
        </div>
    {/if}
</main>