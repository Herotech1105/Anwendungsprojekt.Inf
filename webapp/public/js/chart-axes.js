import { getChartColors } from "./chart-colors.js";

export function getAxesConfig(tickIntervalMs) {
    const c = getChartColors();

    return {
        x: {
            type: "time",
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
                autoSkip: true,
                autoSkipPadding: 20,
                maxTicksLimit: tickIntervalMs ? undefined : 8,

                callback: function(value, index, ticks) {
                    const ts = ticks[index].value;

                    // Wenn kein Intervall → Chart.js entscheidet selbst
                    if (!tickIntervalMs) {
                        const d = new Date(ts);
                        return [
                            d.toLocaleDateString("de-DE"),
                            d.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" })
                        ];
                    }

                    // Nur Ticks anzeigen, die exakt auf das Intervall fallen
                    if (ts % tickIntervalMs === 0) {
                        const d = new Date(ts);
                        return [
                            d.toLocaleDateString("de-DE"),
                            d.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" })
                        ];
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
