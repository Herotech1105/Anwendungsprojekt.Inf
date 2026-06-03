import { getSensorRange } from "./api.js";

const Chart = window.Chart;

let chart = null;
let liveUpdateInterval = null;
let lastFrom = null;
let lastTo = null;

// Statusmeldung anzeigen
function setStatus(message, type = "info") {
    const el = document.getElementById("chartStatus");
    if (!el) return;

    el.textContent = message;
    el.className = "";
    el.classList.add(`status-${type}`);
}

// Farben abhängig vom Theme
function getChartColors() {
    const dark = document.body.classList.contains("dark");

    return {
        text: dark ? "#e5e7eb" : "#111",
        tempLine: dark ? "#f87171" : "#ef4444",
        tempFill: dark ? "rgba(248,113,113,0.2)" : "rgba(239,68,68,0.15)",
        humLine: dark ? "#60a5fa" : "#3b82f6",
        humFill: dark ? "rgba(96,165,250,0.2)" : "rgba(59,130,246,0.15)"
    };
}

async function renderRange(from, to) {
    try {
        lastFrom = from;
        lastTo = to;

        const data = await getSensorRange(from, to);

        if (!data.labels || data.labels.length === 0) {
            if (chart) chart.destroy();
            setStatus("Keine Daten im gewählten Zeitraum", "error");
            return;
        }

        const ctx = document.getElementById("sensorChart").getContext("2d");

        if (chart) chart.destroy();

        const c = getChartColors();

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "Temperatur (°C)",
                        data: data.temperatures,
                        borderColor: c.tempLine,
                        backgroundColor: c.tempFill,
                        borderWidth: 2,
                        fill: true,
                        tension: 0.25
                    },
                    {
                        label: "Luftfeuchtigkeit (%)",
                        data: data.humidities,
                        borderColor: c.humLine,
                        backgroundColor: c.humFill,
                        borderWidth: 2,
                        fill: true,
                        tension: 0.25
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        ticks: {
                            maxRotation: 45,
                            minRotation: 45,
                            color: c.text
                        },
                        grid: {
                            color: c.text + "33"
                        }
                    },
                    y: {
                        ticks: {
                            color: c.text
                        },
                        grid: {
                            color: c.text + "33"
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: c.text
                        }
                    },
                    tooltip: {
                        backgroundColor: "rgba(0,0,0,0.8)",
                        titleColor: "#fff",
                        bodyColor: "#fff"
                    }
                }
            }
        });

        if (to) {
            setStatus(`Statischer Zeitraum geladen, ${data.labels.length} Rohdatensätze`, "success");
        }

    } catch (err) {
        console.error("Chart render error:", err);
        setStatus("Verbindungsproblem, Daten konnten nicht geladen werden", "error");
    }
}

// Chart neu aufbauen (Dark Mode)
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
