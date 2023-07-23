const items = document.querySelectorAll(".item");
const dropdowns = document.querySelectorAll(".dropdown");
const filtersContainer = document.querySelector(".filters");

const macModels = [];
const macMemory = [];
const macCpus = [];

//Generating items with js. So if we will add new items it will also check available filters if it will be new we will create new filters



function generateItems() {
    const modelContainer = document.createElement("div");
    const memoryContainer = document.createElement("div");
    const cpuContainer = document.createElement("div");

    let modelsCategoryAdded = false; // Флаг, который отслеживает, была ли уже добавлена категория "Models"
    let memoryCategoryAdded = false; // Флаг, который отслеживает, была ли уже добавлена категория "Memory"
    let cpuCategoryAdded = false; // Флаг, который отслеживает, была ли уже добавлена категория "Memory"

    items.forEach(item => {
        const modelName = item.querySelector("h4").innerHTML;
        const memoryName = item.querySelector("h5").innerHTML;
        const cpuName = item.querySelector(".Cpu").innerHTML;

        if (!macModels.includes(modelName)) {
            macModels.push(modelName);

            if (!modelsCategoryAdded) {
                const h3 = document.createElement("h3");
                h3.innerHTML = "Models";

                modelContainer.appendChild(h3);
                modelsCategoryAdded = true;
            }

            const li = document.createElement("li");
            li.classList.add("model_");

            const label = document.createElement("label");
            const input_checkbox = document.createElement("input");
            const span_checkbox = document.createElement("span");

            label.classList.add("form-control");
            label.innerHTML = modelName;
            input_checkbox.classList.add("checkbox-basic");
            input_checkbox.type = "checkbox";
            input_checkbox.dataset.type = "name";
            input_checkbox.name = modelName;
            input_checkbox.addEventListener("change", filterItems);
            span_checkbox.classList.add("checkmark");

            label.append(input_checkbox, span_checkbox);
            li.appendChild(label);

            modelContainer.appendChild(li);
        }

        if (!macMemory.includes(memoryName)) {
            macMemory.push(memoryName);

            if (!memoryCategoryAdded) {
                const h3 = document.createElement("h3");
                h3.innerHTML = "Memory";

                memoryContainer.appendChild(h3);
                memoryCategoryAdded = true;
            }

            const li = document.createElement("li");
            li.classList.add("memory_");

            const label = document.createElement("label");
            const input_checkbox = document.createElement("input");
            const span_checkbox = document.createElement("span");

            label.classList.add("form-control");
            label.innerHTML = memoryName;
            input_checkbox.classList.add("checkbox-basic");
            input_checkbox.type = "checkbox";
            input_checkbox.dataset.type = "memory";
            input_checkbox.name = memoryName;
            input_checkbox.addEventListener("change", filterItems);
            span_checkbox.classList.add("checkmark");

            label.append(input_checkbox, span_checkbox);
            li.appendChild(label);

            memoryContainer.appendChild(li);
        }
        if (!macCpus.includes(cpuName)) {
            macCpus.push(cpuName);

            if (!cpuCategoryAdded) {
                const h3 = document.createElement("h3");
                h3.innerHTML = "Cpu";

                cpuContainer.appendChild(h3);
                cpuCategoryAdded = true;
            }

            const li = document.createElement("li");
            li.classList.add("cpu_");

            const label = document.createElement("label");
            const input_checkbox = document.createElement("input");
            const span_checkbox = document.createElement("span");

            label.classList.add("form-control");
            label.innerHTML = cpuName;
            input_checkbox.classList.add("checkbox-basic");
            input_checkbox.type = "checkbox";
            input_checkbox.dataset.type = "cpu";
            input_checkbox.name = cpuName;
            input_checkbox.addEventListener("change", filterItems);
            span_checkbox.classList.add("checkmark");

            label.append(input_checkbox, span_checkbox);
            li.appendChild(label);

            cpuContainer.appendChild(li);
        }
    });

    // Добавляем контейнеры сгруппированных элементов на страницу
    filtersContainer.appendChild(modelContainer);
    filtersContainer.appendChild(memoryContainer);
    filtersContainer.appendChild(cpuContainer);
}

generateItems()

const clearFiltersButton = document.querySelector(".clear-filters");
const inputCheckBoxes = document.querySelectorAll(".checkbox-basic");


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
    const selectedCpu = [];

    inputCheckBoxes.forEach(checkbox => {
        if (checkbox.checked) {
            const label = checkbox.parentNode;
            const labelText = label.textContent.trim();
            //if checkbox is checked we are checking
            // for datatype and then adding our item to arrays.
            // If it's memory we are adding filter to selectedMemory
            // and if it's model we are adding filter to selectedModels
            if (checkbox.dataset.type === "name") {
                selectedModels.push(labelText);
            } else if (checkbox.dataset.type === "memory") {
                selectedMemory.push(labelText);
            } else if (checkbox.dataset.type === "cpu") {
                selectedCpu.push(labelText);
            }
        }
    });

    items.forEach(item => {
        const itemName = item.querySelector(".model").textContent;
        const itemMemory = item.querySelector(".memory").textContent;
        const itemCpu = item.querySelector(".Cpu").textContent;
        let showItem = true;

        if (selectedModels.length > 0 &&
            !selectedModels.some(model => itemName.includes(model))) {
            showItem = false;
        }

        if (selectedMemory.length > 0 && !selectedMemory.includes(itemMemory)) {
            showItem = false;
        }

        if (selectedCpu.length > 0 && !selectedCpu.includes(itemCpu)) {
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

