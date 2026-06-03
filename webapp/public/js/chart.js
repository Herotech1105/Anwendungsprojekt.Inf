import { getSensorRange } from "./api.js";

const Chart = window.Chart;

let chart = null;
let liveUpdateInterval = null;

function setStatus(message, type = "info") {
    const el = document.getElementById("chartStatus");
    if (!el) return;

    el.textContent = message;
    el.className = "";
    el.classList.add(`status-${type}`);
}

async function renderRange(from, to) {
    try {
        const data = await getSensorRange(from, to);

        if (!data.labels || data.labels.length === 0) {
            if (chart) chart.destroy();
            setStatus("Keine Daten im gewählten Zeitraum", "error");
            return;
        }

        const ctx = document.getElementById("sensorChart").getContext("2d");

        if (chart) chart.destroy();

        chart = new Chart(ctx, {
            type: "line",
            data: {
                labels: data.labels,
                datasets: [
                    {
                        label: "Temperatur (°C)",
                        data: data.temperatures,
                        borderColor: "#ef4444",
                        backgroundColor: "rgba(239,68,68,0.15)",
                        borderWidth: 2,
                        fill: true,
                        tension: 0.25
                    },
                    {
                        label: "Luftfeuchtigkeit (%)",
                        data: data.humidities,
                        borderColor: "#3b82f6",
                        backgroundColor: "rgba(59,130,246,0.15)",
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
                            minRotation: 45
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: "#fff",
                            font: {
                                size: 14
                            }
                        }
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

export function initChartEvents() {
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
}
