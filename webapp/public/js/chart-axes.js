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
                    // WICHTIG: echtes Label holen, nicht den Index
                    const rawLabel = this.getLabelForValue(value);
                    // rawLabel ist z.B. "2024-06-03T14:00:00.000Z"
                    const d = new Date(rawLabel);

                    if (isNaN(d.getTime())) {
                        // Falls mal was Komisches kommt, lieber leer
                        return "";
                    }

                    const date = d.toLocaleDateString("de-DE");
                    const time = d.toLocaleTimeString("de-DE", {
                        hour: "2-digit",
                        minute: "2-digit"
                    });

                    const interval = Math.ceil(ticks.length / 8);
                    if (index % interval === 0) {
                        return [date, time]; // zweizeilig
                    }

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
