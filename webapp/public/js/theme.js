// theme.js
import { rebuildChart } from "./chart.js";

export function initThemeToggle() {
    const themeToggle = document.getElementById("themeToggle");
    if (!themeToggle) {
        console.warn("[theme] themeToggle not found");
        return;
    }

    themeToggle.addEventListener("change", () => {
        if (themeToggle.checked) {
            document.body.classList.add("dark");
            console.debug("[theme] switched to dark");
        } else {
            document.body.classList.remove("dark");
            console.debug("[theme] switched to light");
        }

        // Chart neu aufbauen
        rebuildChart();
    });
}
