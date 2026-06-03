import { getSensorRange } from "./api.js";
import { getChartColors } from "./chart-colors.js";
import { getAxesConfig } from "./chart-axes.js";
import { getDatasets } from "./chart-datasets.js";
import { targetRangePlugin } from "./chart-target-plugin.js";
import { formatTimestampParts, getTickIntervalMs } from "./chart-utils.js";

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

/* ---------------------------------------------------
   RANGE BUTTON LOGIK (1h / 10h / 24h)
--------------------------------------------------- */

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

/* ---------------------------------------------------
   CHART RENDERING
--------------------------------------------------- */

export async function renderRange(from, to, rangeHours = null) {
    try {
        lastFrom = from;
        lastTo = to;
        lastRangeHours = rangeHours;

        const data = await getSensorRange(from, to);

        if (!data.labels || data.labels.length === 0) {
            if (chart) chart.destroy();
            setStatus("Keine Daten im gewählten Zeitraum", "error");
            return;
        }

        /* -------------------------------
           ZEITSTEMPEL ZWEIZEILIG FORMATIEREN
        -------------------------------- */
        const formattedLabels = data.labels.map(ts => {
            const { date, time } = formatTimestampParts(ts);
            return [date, time]; // Chart.js interpretiert Arrays als Zeilen
        });

        const ctx = document.getElementById("sensorChart").getContext("2d");

        if (chart) chart.destroy();

        /* -------------------------------
           TICK-INTERVALL BERECHNEN
        -------------------------------- */
        const tickIntervalMs = rangeHours ? getTickIntervalMs(rangeHours) : null;

        /* -------------------------------
           CHART INITIALISIEREN
        -------------------------------- */
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

/* ---------------------------------------------------
   DARK/LIGHT MODE REBUILD
--------------------------------------------------- */

export function rebuildChart() {
    if (!chart || !lastFrom) return;

    renderRange(lastFrom, lastTo || new Date().toISOString(), lastRangeHours);
}

/* ---------------------------------------------------
   LOAD RANGE EVENT (FROM / FROM–TO)
--------------------------------------------------- */

window.addEventListener("loadRange", (e) => {
    const { from, to } = e.detail;

    // Buttons nur anzeigen, wenn NUR FROM gewählt wurde
    if (!to) {
        rangeButtons.style.display = "flex";
    } else {
        rangeButtons.style.display = "none";
    }

    // Live-Modus stoppen
    if (liveUpdateInterval) {
        clearInterval(liveUpdateInterval);
        liveUpdateInterval = null;
    }

    // LIVE-MODUS
    if (!to) {
        setStatus("Live‑Modus aktiv (minütliche Aktualisierung)", "live");

        const now = new Date().toISOString();
        renderRange(from, now);

        liveUpdateInterval = setInterval(() => {
            renderRange(from, new Date().toISOString());
            setStatus(`Live‑Modus aktualisiert: ${new Date().toLocaleTimeString()}`, "live");
        }, 60000);

    } else {
        // FROM–TO → statischer Bereich
        renderRange(from, to);
    }
});
