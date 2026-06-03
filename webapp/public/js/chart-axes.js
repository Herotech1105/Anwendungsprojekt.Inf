import { getChartColors } from "./chart-colors.js";

export function getAxesConfig() {
    const c = getChartColors();

    return {
        x: {
            ticks: {
                color: c.text,
                maxRotation: 45,
                minRotation: 45
            },
            grid: {
                color: c.text + "33"
            }
        },
        y: {
            position: "left",
            ticks: { color: c.text },
            grid: { color: c.text + "33" }
        },
        y1: {
            position: "right",
            ticks: { color: c.text },
            grid: { display: false }
        }
    };
}
