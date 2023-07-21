const clearFiltersButton = document.querySelector(".clear-filters");
const inputCheckBoxes = document.querySelectorAll(".checkbox-basic");
clearFiltersButton.addEventListener("click", () => {
    inputCheckBoxes.forEach(checkbox => {
        checkbox.checked = false;
    });
});