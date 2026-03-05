document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("health-form");
  const resultContainer = document.querySelector(".result_content");

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    resultContainer.innerHTML = "";

    // Collect form data
    const formData = {
      age: parseFloat(document.getElementById("age").value),
      BMIBaseline: parseFloat(document.getElementById("BMIBaseline").value),
      sex: document.getElementById("gender").value,
      diabetes: document.querySelector("input[name='HistoryDiabetes']").checked
        ? 1
        : 0,
      chd: document.querySelector("input[name='HistoryCHD']").checked ? 1 : 0,
      cholesterol: parseFloat(
        document.getElementById("CholesterolBaseline").value
      ),
      creatinine: parseFloat(
        document.getElementById("CreatinineBaseline").value
      ),
      egfr: parseFloat(document.getElementById("eGFRBaseline").value),
      sBP: parseFloat(document.getElementById("sBPBaseline").value),
      dBP: parseFloat(document.getElementById("dBPBaseline").value),
    };

    try {
      const response = await fetch("/prediction", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Server Error:", errorData);
        resultContainer.innerHTML = `<h4 class="error">Error: ${
          errorData.message || "Something went wrong on the server."
        }</h4>`;
        return;
      }

      const data = await response.json();
      resultContainer.innerHTML = `<h4>CKD Probability: ${data.probability}%</h4>`;
      form.reset();
    } catch (error) {
      console.error("Fetch Error:", error);
      resultContainer.innerHTML = `<h4 class="error">Something went wrong. Please try again.</h4>`;
    }
  });
});


document.getElementById("health-form").addEventListener("submit", function(event) {
    event.preventDefault();

    setTimeout(function() {
        // Show the link after results are loaded
        document.getElementById("results-link").style.display = "block";
    }, 2000);
});
