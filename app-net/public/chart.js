import { getSensorRange } from "./frontend.js";

let chart = null;

// Statusmeldung in der Card anzeigen
function setStatus(message) {
    const el = document.getElementById("chartStatus");
    if (el) el.textContent = message;
}

async function renderRange(from, to) {
    try {
        const data = await getSensorRange(from, to);

        // Keine Daten im Zeitraum
        if (!data.labels || data.labels.length === 0) {
            if (chart) chart.destroy();
            setStatus("Keine Daten im gewählten Zeitraum");
            return;
        }

        // Wenn Daten vorhanden => Status löschen
        setStatus("");

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
                        borderColor: "rgba(255, 99, 132, 1)",
                        borderWidth: 2,
                        fill: false,
                        tension: 0.2
                    },
                    {
                        label: "Luftfeuchtigkeit (%)",
                        data: data.humidities,
                        borderColor: "rgba(54, 162, 235, 1)",
                        borderWidth: 2,
                        fill: false,
                        tension: 0.2
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
                }
            }
        });

    } catch (err) {
        console.error("Chart render error:", err);
        setStatus("Verbindungsproblem, Daten konnten nicht geladen werden");
    }
}

window.addEventListener("loadRange", (e) => {
    const { from, to } = e.detail;
    renderRange(from, to);
});
