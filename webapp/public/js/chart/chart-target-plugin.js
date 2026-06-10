// js/chart/chart-target-plugin.js
import { getChartColors } from "./chart-colors.js";

// Colors the background ranges of temperature and humidity before chart is rendered
export const targetRangePlugin = {
    id: "targetRangePlugin",
    beforeDraw(chart) {
        const { ctx, chartArea, scales } = chart;
        const c = getChartColors();

        // Temperature range (19–21 °C)
        const yTemp = scales.y;
        const topTemp = yTemp.getPixelForValue(21);
        const bottomTemp = yTemp.getPixelForValue(19);

        ctx.save();
        ctx.fillStyle = c.tempTargetFill;
        ctx.fillRect(chartArea.left, topTemp, chartArea.right - chartArea.left, bottomTemp - topTemp);
        ctx.restore();

        // Humidity (40–55 %)
        const yHum = scales.y1;
        const topHum = yHum.getPixelForValue(55);
        const bottomHum = yHum.getPixelForValue(40);

        ctx.save();
        ctx.fillStyle = c.humTargetFill;
        ctx.fillRect(chartArea.left, topHum, chartArea.right - chartArea.left, bottomHum - topHum);
        ctx.restore();
    }
};
