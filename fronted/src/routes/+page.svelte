<script lang="ts">
    import api from '$lib/api';
    import { goto } from '$app/navigation';
    import { fly, fade, scale } from 'svelte/transition';
    import { quintOut } from 'svelte/easing';
    import { flip } from 'svelte/animate';
    import { toaster } from '$lib/toast.svelte.js';

    // let responseData = $state<any>(null);
    // let isLoading = $state<boolean>(false);
    // let errorMessage = $state<string | null>(null);

    const { data } = $props();

    let crops = $state<any[]>([]);
    let isResolving = $state(true);

    $effect(() => {
        data.cropsPromise
            .then((res: any[]) => {
                crops = res;
            })
            .catch(() => {
                toaster.add('No se pudo cargar la lista de cultivos', 'error');
            })
            .finally(() => {
                isResolving = false;
            })
    })

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

    const handleDelete = async (id: number) => {
        const cropIndex = crops.findIndex(c => c.id === id);
        if (cropIndex === -1) return;

        try {
            await api.delete(`/crops/${id}/`);
            crops = crops.filter(c => c.id !== id);
            toaster.add('Cultivo eliminado de la base de datos.', 'success');
        } catch (error) {
            toaster.add('Fallo al intentar eliminar el cultivo', 'error');
        }
    }
</script>

<main class="min-h-screen bg-slate-50">
    <header class="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white px-8 py-4 shadow-sm">
        <div>
            <h1 class="text-2xl font-black text-slate-900 tracking-tight mb-1">Agrotech Panel</h1>
            <p class="text-xs font-semibold uppercase tracking-widest text-slate-500">Gestor de Cultivos</p>
        </div>

        <div class="flex items-center gap-4">
            <a href="/crops/new" class="rounded-lg bg-emerald-600 px-5 py-2 text-sm font-bold text-white hover:bg-emerald-700 transition-colors">+ Nuevo Cultivo</a>
            <button onclick={handleLogout} class="cursor-pointer rounded-full bg-slate-100 px-5 py-2 text-sm font-bold text-slate-700 hover:bg-red-50 hover:text-red-600 transitions-colors">
                Cerrar Sesión
            </button>
        </div>
    </header>


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
        {#if isResolving}
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {#each Array(8) as _}
                    <article class="flex h-[220px] animate-pulse flex-col rounded-2xl border border-slate-200 overflow-hidden bg-slate-100">
                        <div class="h-16 w-full bg-slate-200"></div>
                        <div class="flex-1 p-5">
                            <div class="mb-2 h-3 w-24 rounded bg-slate-300"></div>
                            <div class="mb-6 h-4 w-32 rounded bg-slate-300"></div>
                            <div class="flex gap-2">
                                <div class="h-9 w-full rounded-lg bg-slate-200"></div>
                                <div class="h-9 w-full rounded-lg bg-slate-200"></div>
                            </div>
                        </div>
                    </article>
                {/each}   
            </div>



            <!-- <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {#each data.crops as crop (crop.id)}
                    <article class="flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-lg transition-shadow">
                        <div class="bg-emerald-50 px-5 py-4 border-b border-emerald-10">
                            <h2 class="truncate text-lg font-bold text-emerald-900">{crop.name}</h2>
                            <p class="text-xs font-medium text-emerald-600">ID Registro: #{crop.id}</p>
                        </div>

                        <div class="p-5 flex-1 flex flex-col justify-between">
                            <div class="mb-6">
                                <p class="mb-1 text-xs font-semibold uppercase tracking-widest text-slate-400">Fecha de Siembra</p>
                                <p class="font-medium text-slate-800">{crop.sowing_date}</p>
                            </div>

                            <div class="flex gap-2">
                                <a href="/crops/{crop.id}" class="flex-1 rounded-lg border border-slate-200 bg-slate-50 py-2 text-center text-sm font-bold text-slate-600 hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700 transitions-colors">Detalles</a>

                                <a href="/crops/{crop.id}/edit" class="flex-1 rounded-lg border border-slate-200 bg-slate-50 py-2 text-center text-sm font-bold text-slate-600 hover:border-amber-200 hover:bg-amber-50 hover:text-amber-700 transitions-colors">Editar</a>
                            </div>
                        </div>
                    </article>
                {/each}
            </div> -->

        {:else if crops.length === 0}
            <div in:fade={{ duration: 400 }} class="flex flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-white py-20">
                <h3 class="text-lg font-bold text-slate-700">No hay cultivos registrados</h3>
            </div>
        {:else}
            <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                {#each crops as crop, i (crop.id)}
                    <article 
                        in:fly={{ y: 30, duration: 500, delay: i * 50, easing: quintOut }}
                        out:scale={{ duration: 250, start: 0.5, opacity: 0, easing: quintOut }}
                        animate:flip={{ duration: 300, easing: quintOut }}
                        class="group flex flex-col bg-white rounded-2xl border border-slate-200 overflow-hidden hover:shadow-lg transition-shadow"
                    >
                        <div class="bg-emerald-50 px-5 py-4 border-b border-emerald-10">
                            <h2 class="truncate text-lg font-bold text-emerald-900">{crop.name}</h2>
                            <p class="text-xs font-medium text-emerald-600">ID Registro: #{crop.id}</p>
                        </div>

                        <div class="p-5 flex-1 flex flex-col justify-between">
                            <div class="mb-6">
                                <p class="mb-1 text-xs font-semibold uppercase tracking-widest text-slate-400">Fecha de Siembra</p>
                                <p class="font-medium text-slate-800">{crop.sowing_date}</p>
                            </div>

                            <div class="flex flex-wrap gap-2">
                                <a href="/crops/{crop.id}" class="flex-1 rounded-lg border border-slate-200 bg-slate-50 py-2 text-center text-sm font-bold text-slate-600 hover:border-indigo-200 hover:bg-indigo-50 hover:text-indigo-700 transitions-colors">Detalles</a>

                                <a href="/crops/{crop.id}/edit" class="flex-1 rounded-lg border border-slate-200 bg-slate-50 py-2 text-center text-sm font-bold text-slate-600 hover:border-amber-200 hover:bg-amber-50 hover:text-amber-700 transitions-colors">Editar</a>

                                <button onclick={() => handleDelete(crop.id)} class="w-full cursor-pointer rounded-lg border border-slate-200 bg-white py-2 text-center text-sm font-bold text-slate-600 transition-colors hover:border-red-200 hover:bg-red-50">
                                    Eliminar
                                </button>
                            </div>
                        </div>
                    </article>
                {/each}
            </div>
        {/if}
    </section>

</main>