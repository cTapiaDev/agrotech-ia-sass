<script lang="ts">
    import api from '$lib/api';
    import { goto } from '$app/navigation';

    let username = $state('');
    let password = $state('');
    let errorMessage = $state<string | null>(null);
    let isLoading = $state(false);

    const handleLogin = async (event: Event) => {
        event.preventDefault();
        isLoading = true;
        errorMessage = null;

        try {
            const response = await api.post('/token/', {
                username,
                password
            });

            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);

            goto('/');
        } catch (error) {
            errorMessage = 'Credenciales inválidas.'
        } finally {
            isLoading = false;
        }
    }
</script>

<div class="flex min-h-screen items-center justify-center bg-slate-100 p-4">
    <form class="flex max-w-sm flex-col rounded-xl bg-white p-8 shadow-xl" onsubmit={handleLogin}>
        <h2 class="mb-6 text-2xl font-bold text-slate-800">Iniciar Sesión</h2>

        {#if errorMessage}
            <div class="mb-4 rounded bg-red-100 p-3 text-sm text-red-700">
                {errorMessage}
            </div>
        {/if}

        <label class="mb-2 text-sm font-semibold text-slate-600" for="username">Usuario</label>
        <input type="text" id="username" bind:value={username} required class="mb-4 rounded-md border border-slate-300 px-3 py-2 outline-none" >

        <label class="mb-2 text-sm font-semibold text-slate-600" for="password">Contraseña</label>
        <input type="password" id="password" bind:value={password} required class="mb-4 rounded-md border border-slate-300 px-3 py-2 outline-none" >

        <button
            type="submit"
            disabled={isLoading}
            class="cursor-pointer rounded-lg bg-indigo-600 px-6 py-3 font-semibold text-white shadow-sm transition-all hover:bg-indigo-700"
        >
            {isLoading ? 'Conectando...' : 'Entrar'}
        </button>
    </form>
</div>