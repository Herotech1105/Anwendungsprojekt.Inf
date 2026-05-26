// chart.js
let sensorChart = null;

function updateChart(data) {
  const ctx = document.getElementById("sensorChart").getContext("2d");

  const labels = data.map((row) =>
    new Date(row.timestamp).toLocaleString("de-DE")
  );
  const values = data.map((row) => row.value);

  if (sensorChart) {
    sensorChart.data.labels = labels;
    sensorChart.data.datasets[0].data = values;
    sensorChart.update();
    return;
  }

  sensorChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Sensorwert",
          data: values,
          borderColor: "rgba(75, 192, 192, 1)",
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          tension: 0.1,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: {
            display: true,
            text: "Zeit",
          },
        },
        y: {
          title: {
            display: true,
            text: "Wert",
          },
        },
      },
    },
  });
}
