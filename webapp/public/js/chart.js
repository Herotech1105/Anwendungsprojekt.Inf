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

if (rangeButtons) {
    rangeButtons.addEventListener("click", (e) => {
        if (!e.target.dataset.range) return;
        const hours = Number(e.target.dataset.range);
        lastRangeHours = hours;
        const toMs = Date.now();
        const fromMs = Date.now() - hours * 60 * 60 * 1000;
        console.debug("[chart] range button clicked", { hours, fromMs, toMs });
        renderRange({ fromMs, toMs }, hours);
    });
}

function parseLabelToDate(label) {
    if (label == null) return null;
    if (typeof label === "number" || (/^\d+$/.test(String(label)) && String(label).length > 9)) {
        const d = new Date(Number(label));
        if (!isNaN(d.getTime())) return d;
    }
    if (typeof label === "string") {
        const d = new Date(label);
        if (!isNaN(d.getTime())) return d;
    }
    return null;
}

export async function renderRange(params, rangeHours = null) {
    try {
        lastFrom = params.fromMs ?? params.from;
        lastTo = params.toMs ?? params.to;
        lastRangeHours = rangeHours;

        console.debug("[chart] renderRange called with params", params, "rangeHours", rangeHours);

        const data = await getSensorRange(params);

        if (!data || !Array.isArray(data.labels) || data.labels.length === 0) {
            if (chart) chart.destroy();
            setStatus("Keine Daten im gewählten Zeitraum", "error");
            console.warn("[chart] no data returned from API");
            return;
        }

        // Debug-Log: erstes Label und wie es geparst wird
        console.debug("[chart] API first label", data.labels[0], "parsed", parseLabelToDate(data.labels[0]));

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
                scales: getAxesConfig(tickIntervalMs),
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
                                return d.toLocaleString("de-DE");
                            }
                        }
                    }
                }
            },
            plugins: [targetRangePlugin]
        });

        if (params.toMs || params.to) {
            setStatus(`Zeitraum geladen (${data.labels.length} Werte)`, "success");
        }

    } catch (err) {
        console.error("Chart render error:", err);
        setStatus("Verbindungsproblem", "error");
    }
}

export function rebuildChart() {
    if (!chart || !lastFrom) return;
    console.debug("[chart] rebuildChart called", { lastFrom, lastTo, lastRangeHours });
    renderRange({ fromMs: lastFrom, toMs: lastTo ?? Date.now() }, lastRangeHours);
}

window.addEventListener("loadRange", (e) => {
    const detail = e.detail || {};
    const params = {};
    if (detail.fromMs != null) params.fromMs = detail.fromMs;
    else if (detail.from != null) params.from = detail.from;

    if (detail.toMs != null) params.toMs = detail.toMs;
    else if (detail.to != null) params.to = detail.to;

    console.debug("[chart] loadRange event received", params);

    if (rangeButtons) {
        if (!params.to && !params.toMs) {
            rangeButtons.style.display = "flex";
        } else {
            rangeButtons.style.display = "none";
        }
    }

    if (liveUpdateInterval) {
        clearInterval(liveUpdateInterval);
        liveUpdateInterval = null;
    }

    if (!params.to && !params.toMs) {
        setStatus("Live‑Modus aktiv (minütliche Aktualisierung)", "live");
        const nowMs = Date.now();
        renderRange({ fromMs: params.fromMs, toMs: nowMs });
        liveUpdateInterval = setInterval(() => {
            renderRange({ fromMs: params.fromMs, toMs: Date.now() });
            setStatus(`Live‑Modus aktualisiert: ${new Date().toLocaleTimeString()}`, "live");
        }, 60000);
    } else {
        renderRange(params);
    }
});
