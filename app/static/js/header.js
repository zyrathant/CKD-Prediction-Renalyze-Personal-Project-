document
  .querySelector("#dropdown-button")
  .addEventListener("click", function () {
    const dropdown = document.querySelector(".dropdown");
    dropdown.classList.toggle("active");
  });

const menuItems = document.querySelectorAll(".dropdown-content a");
menuItems.forEach(function (item) {
  item.addEventListener("click", function () {
    document.querySelector(".dropdown").classList.remove("active");
  });
});