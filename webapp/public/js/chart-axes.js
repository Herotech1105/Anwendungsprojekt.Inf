import { getChartColors } from "./chart-colors.js";

export function getAxesConfig(tickIntervalMs) {
    const c = getChartColors();

    return {
        x: {
            type: "category",

            ticks: {
                color: c.text,
                maxRotation: 0,
                autoSkip: false,
                font: {
                    weight: "600",
                    size: 12
                },

                callback: function(value, index, ticks) {
                    const ts = ticks[index].value;
                    const d = new Date(ts);

                    const date = d.toLocaleDateString("de-DE");
                    const time = d.toLocaleTimeString("de-DE", {
                        hour: "2-digit",
                        minute: "2-digit"
                    });

                    // FROM–TO → automatisch filtern
                    if (!tickIntervalMs) {
                        const interval = Math.ceil(ticks.length / 8);
                        if (index % interval === 0) return [date, time];
                        return "";
                    }

                    // Range‑Buttons → Intervall nutzen
                    const interval = Math.ceil(ticks.length / 8);
                    if (index % interval === 0) return [date, time];

                    return "";
                }
            },

            grid: {
                color: c.text + "33"
            }
        },

        y: {
            position: "left",
            title: {
                display: true,
                text: "Temperatur (°C)",
                color: c.text,
                font: { weight: "600", size: 14 }
            },
            ticks: {
                color: c.text,
                font: { weight: "600", size: 12 }
            },
            grid: { color: c.text + "33" }
        },

        y1: {
            position: "right",
            title: {
                display: true,
                text: "Luftfeuchtigkeit (%)",
                color: c.text,
                font: { weight: "600", size: 14 }
            },
            ticks: {
                color: c.text,
                font: { weight: "600", size: 12 }
            },
            grid: { display: false }
        }
    };
}
