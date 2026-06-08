// chart-axes.js
import { getChartColors } from "./chart-colors.js";

/**
 * Parst verschiedene Label-Formate in ein Date-Objekt:
 * - ISO-Z (2024-06-03T19:30:00.000Z)
 * - ISO ohne Z (2024-06-03T19:30:00) -> treated as local
 * - numeric (unix ms)
 */
function parseLabelToDate(label) {
    if (label == null) return null;

    // numeric (unix ms)
    if (typeof label === "number" || /^\d+$/.test(String(label))) {
        const ms = Number(label);
        const d = new Date(ms);
        if (!isNaN(d.getTime())) return d;
    }

    // string
    if (typeof label === "string") {
        // ISO-Z (UTC)
        const dUtc = new Date(label);
        if (!isNaN(dUtc.getTime())) {
            // Wenn string endet mit 'Z' oder enthält timezone, Date interpretiert korrekt.
            // Wenn string ist ISO ohne Z, Date interpretiert als local in most browsers.
            return dUtc;
        }
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
                    if (!d) return "";

                    // Lokale Darstellung: Datum / Zeit (z.B. "03.06.2024" / "19:30")
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
