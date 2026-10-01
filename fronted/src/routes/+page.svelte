<script lang="ts">
    // import api from '$lib/api';
    import { goto } from '$app/navigation';

    // let responseData = $state<any>(null);
    // let isLoading = $state<boolean>(false);
    // let errorMessage = $state<string | null>(null);

    const { data } = $props();

    // $effect(() => {
    //     const token = localStorage.getItem('access_token');
    //     if (!token) {
    //         goto('/login');
    //     }
    // });

    // const fetchCropsData = async () => {
    //     isLoading = true;
    //     errorMessage = null;

    //     try {
    //         const response = await api.get('/crops/');
    //         responseData = response.data;
    //     } catch (error: any) {
    //         errorMessage = error.response.status === 401
    //             ? 'Sesión expirada'
    //             : 'Error al comunicarse con el servidor.';
    //         responseData = null;
    //     } finally {
    //         isLoading = false;
    //     }
    // }

    const handleLogout = () => {
        localStorage.clear();
        goto('/login');
    }
</script>

<main class="flex min-h-screen flex-col items-center bg-slate-50 p-6">
    <div class="flex w-full max-w-3xl items-center justify-between">
        <h1 class="text-4xl font-extrabold text-slate-900 tracking-tight mb-8">Svelte</h1>
        <button onclick={handleLogout}>
            Cerrar Sesión
        </button>
    </div>


    <!-- <button 
        class="cursor-pointer rounded-lg bg-indigo-600 px-6 py-3 font-semibold text-white shadow-sm transition-all hover:bg-indigo-700"
        onclick={fetchCropsData}
        disabled={isLoading}
    >
        {isLoading ? 'Conectando...' : 'Obtener Cultivos'}
    </button> -->

    <!-- {#if errorMessage}
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
    {/if} -->

    <section class="max-w-7xl mx-auto px-8 py-10">
        {#if data.crops.length === 0}
            <h3>No hay cultivos registrados.</h3>
        {:else}
            <div class="grid grid-cols-3 gap-6">
                {#each data.crops as crop (crop.id)}
                    <article class="flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden">
                        <div class="bg-emerald-50 px-5 py-4 border-b border-emerald-10">
                            <h2 class="text-lg font-bold text-emerald-900">{crop.name}</h2>
                            <p class="text-xs font-medium text-emerald-600">ID Registro: #{crop.id}</p>
                        </div>

                        <div class="p-5 flex-1 flex flex-col justify-between">
                            <div>
                                <p>Fecha de Siembra</p>
                                <p>{crop.sowing_date}</p>
                            </div>
                        </div>
                    </article>
                {/each}
            </div>
        {/if}
    </section>

</main>