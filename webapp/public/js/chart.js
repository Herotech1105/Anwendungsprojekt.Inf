import { getSensorRange } from "./api.js";
import { getChartColors } from "./chart-colors.js";
import { getAxesConfig } from "./chart-axes.js";
import { getDatasets } from "./chart-datasets.js";
import { targetRangePlugin } from "./chart-target-plugin.js";
import { formatTimestampParts } from "./chart-utils.js";

const Chart = window.Chart;

let chart = null;
let liveUpdateInterval = null;
let lastFrom = null;
let lastTo = null;

function setStatus(message, type = "info") {
    const el = document.getElementById("chartStatus");
    if (!el) return;

    el.textContent = message;
    el.className = "";
    el.classList.add(`status-${type}`);
}

export async function renderRange(from, to) {
    try {
        lastFrom = from;
        lastTo = to;

        const data = await getSensorRange(from, to);

        if (!data.labels || data.labels.length === 0) {
            if (chart) chart.destroy();
            setStatus("Keine Daten im gewählten Zeitraum", "error");
            return;
        }

        // Zeitstempel formatieren → zweizeilig (Datum oben, Uhrzeit unten)
        const formattedLabels = data.labels.map(ts => {
            const { date, time } = formatTimestampParts(ts);
            return [date, time]; // Chart.js interpretiert Arrays als Zeilen
        });

        const ctx = document.getElementById("sensorChart").getContext("2d");

        if (chart) chart.destroy();

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: formattedLabels,
                datasets: getDatasets(data)
            },
            options: {
                responsive: true,
                scales: getAxesConfig(),
                plugins: {
                    legend: {
                        labels: {
                            color: getChartColors().text,
                            font: {
                                weight: "600",
                                size: 14
                            }
                        }
                    }
                }
            },
            plugins: [targetRangePlugin]
        });

        if (to) {
            setStatus(`Statischer Zeitraum geladen, ${data.labels.length} Rohdatensätze`, "success");
        }

    } catch (err) {
        console.error("Chart render error:", err);
        setStatus("Verbindungsproblem, Daten konnten nicht geladen werden", "error");
    }
}

export function rebuildChart() {
    if (!chart || !lastFrom) return;
    renderRange(lastFrom, lastTo || new Date().toISOString());
}

window.addEventListener("loadRange", (e) => {
    const { from, to } = e.detail;

    if (liveUpdateInterval) {
        clearInterval(liveUpdateInterval);
        liveUpdateInterval = null;
    }

    if (!to) {
        setStatus("Live‑Modus aktiv (minütliche Aktualisierung)", "live");

        renderRange(from, new Date().toISOString());

        liveUpdateInterval = setInterval(() => {
            renderRange(from, new Date().toISOString());
            setStatus(`Live‑Modus aktualisiert: ${new Date().toLocaleTimeString()}`, "live");
        }, 60000);

    } else {
        renderRange(from, to);
    }
});
