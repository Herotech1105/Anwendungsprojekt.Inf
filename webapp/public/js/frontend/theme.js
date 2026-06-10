// js/frontend/theme.js
import { rebuildChart } from "../chart/chart.js";

export function initThemeToggle() {
    const toggle = document.getElementById("themeToggle");

    toggle.addEventListener("change", () => {
        document.body.classList.toggle("dark", toggle.checked);
        rebuildChart();
    });
}
