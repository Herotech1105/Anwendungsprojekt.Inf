import { getChartColors } from "./chart-colors.js";

export function getAxesConfig() {
    const c = getChartColors();

    return {
        x: {
            ticks: {
                color: c.text,
                autoSkip: true,
                maxTicksLimit: 8
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
                color: c.text
            },
            ticks: { color: c.text },
            grid: { color: c.text + "33" }
        },
        y1: {
            position: "right",
            title: {
                display: true,
                text: "Luftfeuchtigkeit (%)",
                color: c.text
            },
            ticks: { color: c.text },
            grid: { display: false }
        }
    };
}
