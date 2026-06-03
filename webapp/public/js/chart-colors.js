export function getChartColors() {
    const dark = document.body.classList.contains("dark");

    return {
        text: dark ? "#e5e7eb" : "#111",

        tempLine: dark ? "#f87171" : "#ef4444",
        humLine: dark ? "#60a5fa" : "#3b82f6",

        tempTargetFill: dark ? "rgba(34,197,94,0.15)" : "rgba(34,197,94,0.25)",
        humTargetFill: dark ? "rgba(234,179,8,0.15)" : "rgba(234,179,8,0.25)"
    };
}
