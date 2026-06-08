// chart-axes.js
import { getChartColors } from "./chart-colors.js";

function parseLabelToDate(label) {
    if (label == null) return null;

    if (typeof label === "number" || (/^\d+$/.test(String(label)) && String(label).length > 9)) {
        const ms = Number(label);
        const d = new Date(ms);
        if (!isNaN(d.getTime())) return d;
    }

    if (typeof label === "string") {
        const d = new Date(label);
        if (!isNaN(d.getTime())) return d;
    }

    return null;
}

export function getAxesConfig(tickIntervalMs) {
    const c = getChartColors();

    return {
        x: {
            type: "category",
            ticks: {
                color: c.text,
                maxRotation: 0,
                autoSkip: false,
                font: { weight: "600", size: 12 },

                callback: function(value, index, ticks) {
                    const rawLabel = this.getLabelForValue(value);
                    if (!rawLabel) return "";

                    const d = parseLabelToDate(rawLabel);
                    if (!d) {
                        console.debug("[chart-axes] could not parse label", rawLabel);
                        return "";
                    }

                    const date = d.toLocaleDateString("de-DE");
                    const time = d.toLocaleTimeString("de-DE", { hour: "2-digit", minute: "2-digit" });

                    const interval = Math.max(1, Math.ceil(ticks.length / 8));
                    if (index % interval === 0) return [date, time];
                    return "";
                }
            },
            grid: { color: c.text + "33" }
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
