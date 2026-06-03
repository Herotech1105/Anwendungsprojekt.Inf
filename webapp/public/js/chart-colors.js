export function getChartColors() {
    const dark = document.body.classList.contains("dark");

    return {
        text: dark ? "#e5e7eb" : "#111",

        tempLine: dark ? "#fca5a5" : "#ef4444",
        humLine: dark ? "#93c5fd" : "#3b82f6",

        // Zielbereiche
        tempTargetFill: dark ? "rgba(239,68,68,0.15)" : "rgba(239,68,68,0.25)",   // ROT
        humTargetFill: dark ? "rgba(59,130,246,0.15)" : "rgba(59,130,246,0.25)"  // BLAU
    };
}
