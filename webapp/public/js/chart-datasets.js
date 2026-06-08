// chart-datasets.js
import { getChartColors } from "./chart-colors.js";

export function getDatasets(data) {
    const c = getChartColors();

    // Debug: show dataset lengths
    console.debug("[chart-datasets] temperatures length", data.temperatures ? data.temperatures.length : 0,
                  "humidities length", data.humidities ? data.humidities.length : 0);

    return [
        {
            label: "Temperatur (°C)",
            data: data.temperatures,
            borderColor: c.tempLine,
            borderWidth: 2,
            fill: false,
            tension: 0.25,
            yAxisID: "y"
        },
        {
            label: "Luftfeuchtigkeit (%)",
            data: data.humidities,
            borderColor: c.humLine,
            borderWidth: 2,
            fill: false,
            tension: 0.25,
            yAxisID: "y1"
        }
    ];
}
