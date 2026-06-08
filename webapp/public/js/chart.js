// statt: const formattedLabels = data.labels.map(...);
const formattedLabels = data.labels;

chart = new Chart(ctx, {
    type: "line",
    data: {
        labels: formattedLabels,
        datasets: getDatasets(data)
    },
    options: {
        responsive: true,
        scales: getAxesConfig(tickIntervalMs),
        plugins: {
            legend: {
                labels: {
                    color: getChartColors().text,
                    font: { weight: "600", size: 14 }
                }
            },
            tooltip: {
                callbacks: {
                    title: (items) => {
                        const rawLabel = items[0].label; // echtes Label
                        const d = new Date(rawLabel);
                        if (isNaN(d.getTime())) return rawLabel;
                        return d.toLocaleString("de-DE");
                    }
                }
            }
        }
    },
    plugins: [targetRangePlugin]
});
