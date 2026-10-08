<script lang="ts">
    import * as d3 from 'd3';

    const { data } = $props();

    const formattedDate = d3.timeFormat("%d/%m/%Y %H:%M");

    const processedLogs = $derived(
        (Array.isArray(data.logs) ? data.logs : []).map((log) => {
            const parsedDate = new Date(log.created_at);

            return {
                ...log,
                formattedDate: isNaN(parsedDate.getTime()) ? '--' : formattedDate(parsedDate)
            }
        })
    )
</script>

<main class="min-h-screen bg-slate-900 p-8">
    <div class="mx-auto max-w-4xl">
        <div>
            <div class="grid grid-cols-3 bg-slate-100 p-3 text-sm font-bold text-slate-500">
                <span>Parcela ID</span>
                <span>Temperatura</span>
                <span>Viento / Fecha</span>
            </div>

            {#if processedLogs.length === 0}
                <div>
                    No hay registros de clima.
                </div>
            {:else}
                <div class="flex flex-col bg-slate-800">
                    {#each processedLogs as log, i (log.farm_field_id + '-' + i)}
                        <div class="grid grid-cols-3 items-center border-b border-slate-700 p-4 text-sm text-slate-300">
                            <span class="font-medium text-white">#{log.farm_field_id}</span>

                            <span class={log.is_successful ? 'text-emerald-400' : 'text-red-400'}>{log.temperature}°C</span>

                            <div class="flex flex-col">
                                <span>{log.wind_speed} km/h</span>
                                <span class="text-xs text-slate-500">{log.formattedDate}</span>
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        </div>
    </div>
</main>