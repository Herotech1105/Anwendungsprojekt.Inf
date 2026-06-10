// js/chart/chart-axes.js
import { getChartColors } from "./chart-colors.js";

/*
* Configuration of chart axes x and y
*/
export function getAxesConfig() {
    const c = getChartColors();

    return {
        x: {
            type: "category",
            ticks: {
                color: c.text,
                maxRotation: 0,
                autoSkip: true,
                font: { weight: "600", size: 12 },
                callback: function (value) {
                    const raw = this.getLabelForValue(value);
                    const d = new Date(raw);
                    if (isNaN(d.getTime())) return raw;

                    const date = d.toLocaleDateString("de-DE");
                    const time = d.toLocaleTimeString("de-DE", {
                        hour: "2-digit",
                        minute: "2-digit"
                    });

                    // zweizeilig: erste Zeile Datum, zweite Zeile Uhrzeit
                    return [date, time];
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
