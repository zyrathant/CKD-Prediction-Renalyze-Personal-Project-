const ctx = document.getElementById("ckdChart").getContext("2d");
const ckdChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["Men", "Women", "Total CKD Cases"],
    datasets: [
      {
        label: "CKD Statistics",
        data: [12, 14, 35.5], 
        backgroundColor: [
          "rgba(54, 162, 235, 0.2)",
          "rgba(255, 99, 132, 0.2)",
          "rgba(75, 192, 192, 0.2)",
        ],
        borderColor: [
          "rgba(54, 162, 235, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(75, 192, 192, 1)",
        ],
        borderWidth: 1,
      },
    ],
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Percentage (%)' 
        }
      },
      x: {
        title: {
          display: true,
          text: 'Gender / Total CKD Cases'
        }
      }
    },
  },
});