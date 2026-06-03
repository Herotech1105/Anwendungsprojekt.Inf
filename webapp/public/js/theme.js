import { rebuildChart } from "./chart.js";

export function initThemeToggle() {
    const themeToggle = document.getElementById("themeToggle");

    themeToggle.addEventListener("change", () => {
        if (themeToggle.checked) {
            document.body.classList.add("dark");
        } else {
            document.body.classList.remove("dark");
        }

        // Chart neu aufbauen
        rebuildChart();
    });
}
