// js/chart/chart-datasets.js
import { getChartColors } from "./chart-colors.js";

/*
* Visual y-axes of temperature and humidity ranges for chart
*/
export function getDatasets(data) {
    const c = getChartColors();

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
