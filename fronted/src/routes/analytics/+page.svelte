<script lang="ts">
    import * as d3 from 'd3';
    import jsPDF from 'jspdf';
    import autoTable from 'jspdf-autotable';

    const { data } = $props();

    const formattedDate = d3.timeFormat("%d/%m/%Y %H:%M");
    const axisTimeFormat = d3.timeFormat("%d/%m %H:%M");

    const processedLogs = $derived(
        (Array.isArray(data.logs) ? data.logs : []).map((log) => {
            const parsedDate = new Date(log.created_at);

            return {
                ...log,
                parsedDate,
                formattedDate: isNaN(parsedDate.getTime()) ? '--' : formattedDate(parsedDate)
            }
        })
        .sort((a, b) => a.parsedDate.getTime() - b.parsedDate.getTime())
    )

    let chartContainer = $state<HTMLElement | null>(null);

    let tooltipVisible = $state(false);
    let tooltipData = $state<any>(null);
    let tooltipX = $state(0);
    let tooltipY = $state(0);

    const downloadChart = () => {
        if (!chartContainer) return;
        const svgElement = chartContainer.querySelector('svg');
        if (!svgElement) return;

        const serializer = new XMLSerializer();
        let svgString = serializer.serializeToString(svgElement);

        svgString = svgString.replace('<svg ', '<svg style="background-color: #20293b; font-family: sans-serif;" ');

        const svgBlob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8'});
        const url = URL.createObjectURL(svgBlob);

        const img = new Image();
        img.onload = () => {
            const canvas = document.createElement('canvas');
            canvas.width = svgElement.clientWidth;
            canvas.height = svgElement.clientHeight;
            const ctx = canvas.getContext('2d');

            if (ctx) {
                ctx.drawImage(img, 0, 0);
                const pngUrl = canvas.toDataURL('image/png');
                const link = document.createElement('a');
                link.href = pngUrl;
                link.download = 'bitacora.png';
                link.click();
            }
            URL.revokeObjectURL(url);
        };
        img.src = url;
    }

    const downLoadPDF = () => {
        const doc = new jsPDF();

        doc.setFontSize(16);
        doc.text("Bitácora Agronómica - Historial", 14, 15);

        const tableData = [...processedLogs].reverse().map(log => [
            `Parcela #${log.farm_field_id}`,
            `${log.temperature}°C`,
            `${log.wind_speed} km/h`,
            log.formattedDate
        ]);

        autoTable(doc, {
            head: [['ID Parcela', 'Temperatura', 'Viento', 'Fecha']],
            body: tableData,
            startY: 22,
            styles: { fontSize: 10, cellPadding: 3 },
            headStyles: { fillColor: [16, 185, 129] },
            alternateRowStyles: { fillColor: [248, 250, 252] }
        });

        doc.save('datos-bitacora')
    }


    $effect(() => {
        if (!chartContainer || processedLogs.length === 0) return;

        d3.select(chartContainer).selectAll('*').remove();

        const margin = { top: 20, right: 30, bottom: 75, left: 60 };
        const width = chartContainer.clientWidth - margin.left - margin.right;
        const height = 300 - margin.top - margin.bottom;

        const svg = d3.select(chartContainer)
            .append('svg')
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        svg.append('defs')
            .append('clipPath')
            .attr('id', 'clip-area-animation')
            .append('rect')
            .attr('width', 0)
            .attr('height', height)

        const minTemp = d3.min(processedLogs, (d) => d.temperature) || 0;
        const maxTemp = d3.max(processedLogs, (d) => d.temperature) || 30;

        const avgTemp = d3.mean(processedLogs, (d) => d.temperature) || 0;
        const maxNode = processedLogs.reduce((prev, current) => (prev.temperature > current.temperature) ? prev : current);
        const minNode = processedLogs.reduce((prev, current) => (prev.temperature < current.temperature) ? prev : current);

        const x = d3.scaleTime()
            .domain(d3.extent(processedLogs, (d) => d.parsedDate) as [Date, Date])
            .range([0, width]);

        const yTemp = d3.scaleLinear()
            .domain([minTemp - 2, maxTemp + 5])
            .range([height, 0]);

        const areaTemp = d3.area<any>()
            .x((d) => x(d.parsedDate))
            .y0(height)
            .y1((d) => yTemp(d.temperature))
            .curve(d3.curveMonotoneX);

        svg.append('path')
            .datum(processedLogs)
            .attr('fill', '#34d399')
            .attr('fill-opacity', 0.2)
            .attr('stroke', 'none')
            .attr('clip-path', 'url(#clip-area-animation)')
            .attr('d', areaTemp);

        svg.select('#clip-area-animation rect')
            .transition()
            .duration(3200)
            .ease(d3.easeCubicOut)
            .attr('width', width)

        svg.append('line')
            .attr('x1', 0)
            .attr('x2', width)
            .attr('y1', yTemp(avgTemp))
            .attr('y2', yTemp(avgTemp))
            .attr('stroke', '#fbbf24')
            .attr('stroke-width', 1.5)
            .attr('stroke-dasharray', '5,5')
            .style('opacity', 0)
            .transition().delay(1000).duration(800)
            .style('opacity', 0.6)

        // Línea principal
        const pathLine = svg.append('path')
            .datum(processedLogs)
            .attr('fill', 'none')
            .attr('stroke', '#10b981')
            .attr('stroke-width', 2.5)
            .attr('d', d3.line<any>()
                .x((d) => x(d.parsedDate))
                .y((d) => yTemp(d.temperature))
                .curve(d3.curveMonotoneX)
            );

        const totalLength = (pathLine.node() as SVGPathElement).getTotalLength();

        pathLine
            .attr('stroke-dasharray', `${totalLength} ${totalLength}`)
            .attr('stroke-dashoffset', totalLength)
            .transition()
            .duration(5200)
            .ease(d3.easeCubicOut)
            .attr('stroke-dashoffset', 0)

        const annotations = svg.append('g')
            .style('opacity', 0)

        // Anotación Máxima
        annotations.append('circle')
            .attr('cx', x(maxNode.parsedDate))
            .attr('cy', yTemp(maxNode.temperature))
            .attr('r', 6)
            .attr('fill', 'none')
            .attr('stroke', '#f87171')
            .attr('stroke-width', 2)

        annotations.append('text')
            .attr('x', x(maxNode.parsedDate))
            .attr('y', yTemp(maxNode.temperature) - 12)
            .attr('text-anchor', 'middle')
            .attr('fill', '#f87171')
            .attr('font-size', '11px')
            .attr('font-weight', 'bold')
            .text(`Peak Calor: ${maxNode.temperature}°C`)

        // Anotación Mínima
        annotations.append('circle')
            .attr('cx', x(minNode.parsedDate))
            .attr('cy', yTemp(minNode.temperature))
            .attr('r', 6)
            .attr('fill', 'none')
            .attr('stroke', '#38bdf8')
            .attr('stroke-width', 2)

        annotations.append('text')
            .attr('x', x(minNode.parsedDate) + 62)
            .attr('y', yTemp(minNode.temperature) + 4)
            .attr('text-anchor', 'middle')
            .attr('fill', '#38bdf8')
            .attr('font-size', '11px')
            .attr('font-weight', 'bold')
            .text(`Mínima: ${minNode.temperature}°C`)

        annotations.transition().delay(2600).duration(600).style('opacity', 1);


        // Eje X
        svg.append('g')
            .attr('transform', `translate(0,${height})`)
            .call(d3.axisBottom(x).ticks(6).tickFormat(axisTimeFormat as any))
            .attr('color', '#64748b')
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em')
            .attr('transform', 'rotate(-45)');

        svg.append('text')
            .attr('transform', `translate(${width / 2}, ${height + margin.bottom - 5})`)
            .style('text-anchor', 'middle')
            .style('fill', '#94a3b8')
            .style('font-size', '12px')
            .style('font-weight', 'bold')
            .text('Fecha de Registro');

        // Eje Y
        svg.append('g')
            .call(d3.axisLeft(yTemp).ticks(5))
            .attr('color', '#64748b');

        svg.append('text')
            .attr('transform', 'rotate(-90)')
            .attr('y', 0 - margin.left + 15)
            .attr('x', 0 - (height / 2))
            .attr('dy', '1em')
            .style('text-anchor', 'middle')
            .style('fill', '#94a3b8')
            .style('font-size', '12px')
            .style('font-weight', 'bold')
            .text('Temperatura (°C)');

        const focus = svg.append('g').style('display', 'none');

        const focusLine = focus.append('line')
            .attr('stroke', '#64748b')
            .attr('stroke-width', 1)
            .attr('stroke-dasharray', '3,3')
            .attr('y1', 0)
            .attr('y2', height);

        const focusCircle = focus.append('circle')
            .attr('r', 5)
            .attr('fill', '#10b981')
            .attr('stroke', '#fff')
            .attr('stroke-width', 2);

        const overlay = svg.append('rect')
            .attr('width', width)
            .attr('height', height)
            .style('fill', 'none')
            .style('pointer-events', 'all');

        const bisectDate = d3.bisector((d: any) => d.parsedDate).left;

        overlay.on('mouseover', () => {
            focus.style('display', null);
            tooltipVisible = true;
        });

        overlay.on('mouseout', () => {
            focus.style('display', 'none');
            tooltipVisible = false;
        });

        overlay.on('mousemove', (event) => {
            const [mouseX] = d3.pointer(event);
            const x0 = x.invert(mouseX);
            
            const i = bisectDate(processedLogs, x0, 1);
            const d0 = processedLogs[i - 1];
            const d1 = processedLogs[i];
            
            if (!d0) return;
            const d = (d1 && d0) ? (x0.getTime() - d0.parsedDate.getTime() > d1.parsedDate.getTime() - x0.getTime() ? d1 : d0) : d0;

            tooltipData = d;
            tooltipX = x(d.parsedDate) + margin.left;
            tooltipY = yTemp(d.temperature) + margin.top;

            focusLine.attr('transform', `translate(${x(d.parsedDate)},0)`);
            focusCircle.attr('transform', `translate(${x(d.parsedDate)},${yTemp(d.temperature)})`);
        });
    });
</script>

<main class="min-h-screen bg-slate-900 p-8">
    <div class="mx-auto max-w-5xl">
        <div class="mb-8 flex items-center justify-between">
            <h2 class="text-3xl font-light text-white">Bitácora Agronómica</h2>

            <div class="flex gap-4">
                <button onclick={downloadChart} class="cursor-pointer rounded-lg border border-slate-600 bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-300 transition-colors hover:bg-slate-700 hover:text-white">
                    Descargar Gráfico
                </button>
                <button onclick={downLoadPDF} class="cursor-pointer rounded-lg border border-slate-600 bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-300 transition-colors hover:bg-slate-700 hover:text-white">
                    Exportar PDF
                </button>
            </div>
        </div>
        
        <div class="relative mb-8 rounded-xl border border-slate-700 bg-slate-800 p-6 shadow-lg">
            <div class="mb-4 text-lg font-semibold text-slate-200">Evolución de Temperatura General</div>

            <div bind:this={chartContainer} class="w-full"></div>
            {#if tooltipVisible && tooltipData}
                <div class="pointer-events-none absolute z-50 rounded-lg border border-slate-600 bg-slate-800/50 p-3 text-sm shadow-xl backdrop-blur-sm" style="left: {tooltipX}px; top: {tooltipY}px; transform: translate(-50%, -100%);">
                    <div class="font-bold mb-1 text-emerald-400 text-lg">{tooltipData.temperature}°C</div>
                    <div class="text-xs text-slate-300">Parcela #{tooltipData.farm_field_id}</div>
                    <div class="text-xs text-slate-400 mb-1">{tooltipData.formattedDate}</div>
                    <div class="text-xs font-semibold text-sky-400">Viento: {tooltipData.wind_speed}</div>
                </div>
            {/if}
        </div>


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