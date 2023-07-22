const items = document.querySelectorAll(".item");
const clearFiltersButton = document.querySelector(".clear-filters");
const inputCheckBoxes = document.querySelectorAll(".checkbox-basic");
const dropdowns = document.querySelectorAll(".dropdown");

//clearing filters
clearFiltersButton.addEventListener("click", () => {
    inputCheckBoxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    filterItems();
});


//filtering items
function filterItems() {
    const selectedModels = [];
    const selectedMemory = [];

    inputCheckBoxes.forEach(checkbox => {
        if (checkbox.checked) {
            const label = checkbox.parentNode;
            const labelText = label.textContent.trim();
            //if checkbox is checked we are cheking
            // for datatype and then adding our item to arrays.
            // If it's memory we are adding filter to selectedMemory
            // and if it's model we are adding filter to selectedModels
            if (checkbox.dataset.type === "name") {
                selectedModels.push(labelText);
            } else if (checkbox.dataset.type === "memory") {
                selectedMemory.push(labelText);
            }
        }
    });

    items.forEach(item => {
        const itemName = item.querySelector(".model").textContent;
        const itemMemory = item.querySelector(".memory").textContent;
        let showItem = true; // Предполагаем, что элемент должен быть показан
        //here is filter logic
        if (selectedModels.length > 0 && !selectedModels.includes(itemName) && !selectedModels.some(model => itemName.startsWith(model))) {
            showItem = false;
        }

        if (selectedMemory.length > 0 && !selectedMemory.includes(itemMemory)) {
            showItem = false;
        }

        if (showItem) {
            item.classList.remove("hidden");
        } else {
            item.classList.add("hidden");
        }
    });
}

//calling function when checkbox is checked or unchecked
inputCheckBoxes.forEach(checkbox => {
    checkbox.addEventListener("change", filterItems);
});

filterItems();


//navbar dropdown's functional
dropdowns.forEach(dropdown => {
    const select = dropdown.querySelector(".select");
    const caret = dropdown.querySelector(".caret");
    const menu = dropdown.querySelector(".menu");
    const options = dropdown.querySelector(".menu li");
    const selected = dropdown.querySelector(".selected");

    select.addEventListener("click", () => {
        select.classList.toggle("select-clicked");
        caret.classList.toggle("caret-rotate");
        menu.classList.toggle("menu-open");
    })
    options.forEach(option_ => {
        option_.addEventListener("click", () => {
            selected.innerHTML = option_.innerText;
            select.classList.remove("select-clicked");
            caret.classList.remove("caret-rotate");
            menu.classList.remove("menu-open");

            options.forEach(option_ => {
                option_.classList.remove("active");
            })
            option_.classList.add("active")
        })
    })
})

