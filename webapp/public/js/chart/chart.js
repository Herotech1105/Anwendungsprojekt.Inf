// js/chart/chart.js
import { getSensorRange } from "../frontend/api.js";
import { getAxesConfig } from "./chart-axes.js";
import { getDatasets } from "./chart-datasets.js";
import { targetRangePlugin } from "./chart-target-plugin.js";
import { getChartColors } from "./chart-colors.js";

const ChartLib = window.Chart;

let chart = null;
let lastFrom = null;
let lastTo = null;


// Sets chart status
function setStatus(type, text) {
    const el = document.getElementById("chartStatus");
    if (!el) return;

    el.className = "";
    if (type) el.classList.add(`status-${type}`);
    el.textContent = text;
}

// Renders the visual chart
export async function renderRange(from, to) {
    lastFrom = from;
    lastTo = to;

    const canvas = document.getElementById("sensorChart");
    const ctx = canvas.getContext("2d");

    try {
        const data = await getSensorRange(from, to);

        if (!data || !data.labels || data.labels.length === 0) {
            if (chart) {
                chart.destroy();
                chart = null;
            }
            canvas.style.display = "none";
            setStatus("info", "Keine Daten im gewählten Zeitraum.");
            return;
        }

        canvas.style.display = "block";

        if (chart) chart.destroy();

        ChartLib.defaults.color = getChartColors().text;

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

        setStatus("success", `${data.labels.length} Werte geladen`);
    } catch (err) {
        if (chart) {
            chart.destroy();
            chart = null;
        }
        canvas.style.display = "none";
        setStatus("error", "Fehler beim Laden der Daten.");
    }
}

// Destroys and rebuilds the Chart
export function rebuildChart() {
    if (lastFrom && lastTo) {
        renderRange(lastFrom, lastTo);
    }
}

window.addEventListener("loadRange", (e) => {
    const { from, to } = e.detail;
    renderRange(from, to);
});
