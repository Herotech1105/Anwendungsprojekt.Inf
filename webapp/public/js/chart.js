// chart.js
import { getSensorRange } from "./api.js";
import { getChartColors } from "./chart-colors.js";
import { getAxesConfig } from "./chart-axes.js";
import { getDatasets } from "./chart-datasets.js";
import { targetRangePlugin } from "./chart-target-plugin.js";
import { getTickIntervalMs } from "./chart-utils.js";

const Chart = window.Chart;

let chart = null;
let liveUpdateInterval = null;
let lastFrom = null;
let lastTo = null;
let lastRangeHours = null;

const rangeButtons = document.getElementById("rangeButtons");

function setStatus(message, type = "info") {
    const el = document.getElementById("chartStatus");
    if (!el) return;
    el.textContent = message;
    el.className = "";
    el.classList.add(`status-${type}`);
}

/* Range Buttons */
if (rangeButtons) {
    rangeButtons.addEventListener("click", (e) => {
        if (!e.target.dataset.range) return;
        const hours = Number(e.target.dataset.range);
        lastRangeHours = hours;
        const to = new Date().toISOString();
        const from = new Date(Date.now() - hours * 60 * 60 * 1000).toISOString();
        renderRange(from, to, hours);
    });
}

/* Hilfsparser für Labels (robust) */
function parseLabelToDate(label) {
    if (label == null) return null;
    if (typeof label === "number" || /^\d+$/.test(String(label))) {
        const d = new Date(Number(label));
        if (!isNaN(d.getTime())) return d;
    }
    if (typeof label === "string") {
        // Wenn string endet mit 'Z' -> UTC; wenn nicht, Date interpretiert meist als lokal
        const d = new Date(label);
        if (!isNaN(d.getTime())) return d;
    }
    return null;
}

/* Render */
export async function renderRange(from, to, rangeHours = null) {
    try {
        lastFrom = from;
        lastTo = to;
        lastRangeHours = rangeHours;

        const data = await getSensorRange(from, to);

        if (!data || !Array.isArray(data.labels) || data.labels.length === 0) {
            if (chart) chart.destroy();
            setStatus("Keine Daten im gewählten Zeitraum", "error");
            return;
        }

        // Labels unverändert übernehmen (Backend liefert lokale Zeitstrings oder numeric timestamps)
        const formattedLabels = data.labels;

        const ctx = document.getElementById("sensorChart").getContext("2d");
        if (chart) chart.destroy();

        const tickIntervalMs = rangeHours ? getTickIntervalMs(rangeHours) : null;

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: formattedLabels,
                datasets: getDatasets(data)
            },
            options: {
                responsive: true,
                scales: getAxesConfig(tickIntervalMs), // Achse formatiert lokal

                plugins: {
                    legend: {
                        labels: {
                            color: getChartColors().text,
                            font: { weight: "600", size: 14 }
                        }
                    },

                    tooltip: {
                        callbacks: {
                            title: (items) => {
                                const rawLabel = items[0].label;
                                const d = parseLabelToDate(rawLabel);
                                if (!d) return rawLabel;
                                // Tooltip lokal anzeigen
                                return d.toLocaleString("de-DE");
                            }
                        }
                    }
                }
            },
            plugins: [targetRangePlugin]
        });

        if (to) {
            setStatus(`Zeitraum geladen (${data.labels.length} Werte)`, "success");
        }

    } catch (err) {
        console.error("Chart render error:", err);
        setStatus("Verbindungsproblem", "error");
    }
}

/* Rebuild */
export function rebuildChart() {
    if (!chart || !lastFrom) return;
    renderRange(lastFrom, lastTo || new Date().toISOString(), lastRangeHours);
}

/* Load range event */
window.addEventListener("loadRange", (e) => {
    const { from, to } = e.detail;

    if (!to) {
        rangeButtons.style.display = "flex";
    } else {
        rangeButtons.style.display = "none";
    }

    if (liveUpdateInterval) {
        clearInterval(liveUpdateInterval);
        liveUpdateInterval = null;
    }

    if (!to) {
        setStatus("Live‑Modus aktiv (minütliche Aktualisierung)", "live");
        const now = new Date().toISOString();
        renderRange(from, now);
        liveUpdateInterval = setInterval(() => {
            renderRange(from, new Date().toISOString());
            setStatus(`Live‑Modus aktualisiert: ${new Date().toLocaleTimeString()}`, "live");
        }, 60000);
    } else {
        renderRange(from, to);
    }
});
