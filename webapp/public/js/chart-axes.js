import { getChartColors } from "./chart-colors.js";

export function getAxesConfig(tickIntervalMs) {
    const c = getChartColors();

    return {
        x: {
            type: "time",

            adapters: {
                date: {} // nutzt Browser‑Date‑Parsing, kein Adapter nötig
            },

            time: {
                tooltipFormat: "dd.MM.yyyy HH:mm",
                displayFormats: {
                    minute: "HH:mm",
                    hour: "HH:mm",
                    day: "dd.MM"
                }
            },

            ticks: {
                color: c.text,
                maxRotation: 0,
                autoSkip: false,

                callback: function(value, index, ticks) {
                    const ts = ticks[index].value;
                    const d = new Date(ts);

                    const date = d.toLocaleDateString("de-DE");
                    const time = d.toLocaleTimeString("de-DE", {
                        hour: "2-digit",
                        minute: "2-digit"
                    });

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
