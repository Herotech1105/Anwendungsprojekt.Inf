// js/chart/chart.js
import { getSensorRange } from "../frontend/api.js";
import { getAxesConfig } from "./chart-axes.js";
import { getDatasets } from "./chart-datasets.js";
import { targetRangePlugin } from "./chart-target-plugin.js";

const ChartLib = window.Chart;

let chart = null;
let lastFrom = null;
let lastTo = null;

export async function renderRange(from, to) {
    lastFrom = from;
    lastTo = to;

    const data = await getSensorRange(from, to);

    if (!data || !data.labels || data.labels.length === 0) {
        document.getElementById("chartStatus").textContent = "Keine Daten";
        return;
    }

    const ctx = document.getElementById("sensorChart").getContext("2d");
    if (chart) chart.destroy();

    chart = new ChartLib(ctx, {
        type: "line",
        data: {
            labels: data.labels,
            datasets: getDatasets(data)
        },
        options: {
            responsive: true,
            scales: getAxesConfig(),
            plugins: {
                legend: {
                    labels: {
                        font: { weight: "600", size: 14 }
                    }
                }
            }
        },
        plugins: [targetRangePlugin]
    });

    document.getElementById("chartStatus").textContent =
        `${data.labels.length} Werte geladen`;
}

export function rebuildChart() {
    if (lastFrom && lastTo) {
        renderRange(lastFrom, lastTo);
    }
}

window.addEventListener("loadRange", (e) => {
    const { from, to } = e.detail;
    renderRange(from, to);
});
