import { getChartColors } from "./chart-colors.js";

/**
 * Axes configuration for Chart.js (category x-axis).
 * Tick callback reads the actual label via this.getLabelForValue(value)
 * and formats it using UTC getters so the chart displays the exact UTC time
 * that was passed in (no local timezone conversion).
 */
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
                    // Get the real label (not the numeric index)
                    const rawLabel = this.getLabelForValue(value);
                    if (!rawLabel) return "";

                    const d = new Date(rawLabel);
                    if (isNaN(d.getTime())) return "";

                    // Format date/time using UTC getters so we show the exact UTC clock time
                    const date =
                        String(d.getUTCDate()).padStart(2, "0") + "." +
                        String(d.getUTCMonth() + 1).padStart(2, "0") + "." +
                        d.getUTCFullYear();

                    const time =
                        String(d.getUTCHours()).padStart(2, "0") + ":" +
                        String(d.getUTCMinutes()).padStart(2, "0");

                    // Limit number of visible ticks (approx. 8)
                    const interval = Math.max(1, Math.ceil(ticks.length / 8));
                    if (index % interval === 0) {
                        return [date, time]; // two-line label: date / time (UTC)
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
