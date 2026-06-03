import { getChartColors } from "./chart-colors.js";

export function getAxesConfig(tickIntervalMs) {
    const c = getChartColors();

    return {
        x: {
            ticks: {
                color: c.text,
                autoSkip: false,
                maxTicksLimit: 8,
                font: {
                    weight: "600",
                    size: 12
                },
                callback: function(value, index, ticks) {
                    if (!tickIntervalMs) return this.getLabelForValue(value);

                    const ts = ticks[index].value;
                    const date = new Date(ts);

                    if (date.getTime() % tickIntervalMs === 0) {
                        return this.getLabelForValue(value);
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
