document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("health-form");
  if (!form) return;

  form.addEventListener("submit", async function (event) {
    event.preventDefault();

    // Select Elements
    const resultBox = document.getElementById("result-container");
    const statusText = document.getElementById("display-status");
    const probText = document.getElementById("display-prob");
    const accent = document.getElementById("risk-accent");
    const recommendation = document.getElementById("display-recommendation");
    const progressBar = document.getElementById("display-progress-bar");
    const submitBtn = form.querySelector('button[type="submit"]');

    // Reset
    resultBox.style.opacity = "0.5"; 
    const originalBtnText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Analyzing... <span class="spinner-border spinner-border-sm"></span>';

    try {
      // Collect Data
      const formData = {
        age: parseFloat(document.getElementById("age").value),
        BMIBaseline: parseFloat(document.getElementById("BMIBaseline").value),
        sex: document.getElementById("gender").value,
        diabetes: document.getElementById("HistoryDiabetes").checked ? 1 : 0,
        chd: document.getElementById("HistoryCHD").checked ? 1 : 0,
        cholesterol: parseFloat(document.getElementById("CholesterolBaseline").value),
        creatinine: parseFloat(document.getElementById("CreatinineBaseline").value),
        egfr: parseFloat(document.getElementById("eGFRBaseline").value),
        sBP: parseFloat(document.getElementById("sBPBaseline").value),
        dBP: parseFloat(document.getElementById("dBPBaseline").value),
      };

      const response = await fetch("/ckd_analysis", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        const isHigh = data.status === "High Risk";
        const themeColor = isHigh ? "#ef4444" : "#10b981";

        statusText.innerText = data.status;
        statusText.style.color = themeColor;
        probText.innerText = data.probability + "%";
        recommendation.innerText = data.recommendation;
        accent.style.backgroundColor = themeColor;

        progressBar.style.width = data.probability + "%";
        progressBar.style.backgroundColor = themeColor;

        resultBox.style.display = "block";
        resultBox.style.opacity = "1"; 
        resultBox.classList.remove("animate__fadeInUp");
        void resultBox.offsetWidth;
        resultBox.classList.add("animate__fadeInUp");

        resultBox.scrollIntoView({ behavior: "smooth", block: "center" });
      } else {
         alert("Error: " + data.error);
      }
    } catch (error) {
      console.error("Fetch Error:", error);
      alert("Something went wrong with the connection.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.innerHTML = originalBtnText;
    }
  });
});