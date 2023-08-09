window.addEventListener('load', solve);
// used to keep state so to refresh when Prices or Discounts Buttons are clicked
let initialState = 0
let initialState2 = 0
function solve() {
    // used to store state of fields prior to edit so when back button is clicked the previous values are restored
    let temp_vals = [0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0]
    // get required DOM elements
    let createOrderBtn = document.getElementById("create-order-btn")
    let showOrderBtn = document.getElementById("show-order-btn")
    let pricesBtn = document.getElementById("prices_btn")
    pricesBtn.addEventListener("click", ListPrices)
    let pricesWindow = document.getElementById("prices-window")
    let discountWindow = document.getElementById("discount-window")
    let ordersWindow = document.getElementById("orders-window")
    // List all data from model when button is clicked
    async function ListPrices(e) {
        e.preventDefault()
        // Check for current sate
        if (initialState === 0) {
            initialState = 1
            initialState2 = 0
            // Hide the Create Order button and show the Show Order Button
            createOrderBtn.style.display = "none"
            createOrderBtn.hidden = true
            showOrderBtn.style.display = "block"
            showOrderBtn.hidden = false
            // Clean the target div and hide the orders div
            pricesWindow.innerHTML = ''
            pricesWindow.style.display = "flex"
            discountWindow.innerHTML = ""
            ordersWindow.style.display = 'none'
            discountWindow.style.display = 'none'
            // Create the HTML elements for adding new items to the model
            let error_li = createElement("li", "", pricesWindow, "error_li", "", {
                "hidden": true,
                "style": "display: none;"
            })
            let create_li = createElement("li", "", pricesWindow, "create_li_id")
            let typeLabel = createElement("label", "Order Type", create_li, "", "", {"for": "type_id"})
            let order_type = createElement("select", "", create_li, "type_id", "", {"name": "type_id",})
            let order_type_options_1 = createElement("option", "Letter", order_type, "", "", {"value": "Letter",})
            let order_type_options_2 = createElement("option", "Parcel", order_type, "", "", {"value": "Parcel",})
            let order_type_options_3 = createElement("option", "Box", order_type, "", "", {"value": "Box",})
            let minLabel = createElement("label", "Min Weight", create_li, "", "", {"for": "min_w_id"})
            let minInput = createElement("input", 0, create_li, "min_w_id", "", {
                    "name": "min_w_id",
                    "type": "text",
                    "onkeypress": "return checkNumber(event)",
                })
            let maxLabel = createElement("label", "Max Weight", create_li, "", "", {"for": "max_w_id"})
            let maxInput = createElement("input", 0, create_li, "max_w_id", "", {
                    "name": "max_w_id",
                    "type": "text",
                    "onkeypress": "return checkNumber(event)",
                })
            let priceLabel = createElement("label", "Price/kg", create_li, "", "", {"for": "price_id"})
            let priceInput = createElement("input", 0, create_li, "price_id", "", {
                    "name": "price_id",
                    "type": "number",
                })
            // Create the button for the PUSH request so that the new item is sent to REST API
            let addBtn = createElement("button", "Create", create_li, "", ["a_button_inside"])
            addBtn.addEventListener("click", addFunc)
            // Create clear button to clear the fields of the create form
            let clearBtn = createElement("button", "Clear", create_li, "", ["a_button_inside"])
            clearBtn.addEventListener("click", clearFunc)
            // Send a GET request to REST API to obtain all prices items from DB
            let res = await fetch(window.URLS.prices)
            let data = await res.json()
            // Sort the obtained DB items first by number, then by letter to represent them sequentially
            let values = Object.values(data).sort(function (a, b) {
                return a.min_weight - b.min_weight}).sort(function (a, b) {
                return a.target_order_type.localeCompare(b.target_order_type)})
            // Create and fill the required HTML elements for each entry from the DB as well as Edit and Delete buttons
            for (let entry of values) {
                let lito = createElement("li", "", pricesWindow, `li_id_${entry["id"]}`)
                let typeLabel = createElement("label", "Order Type", lito, "", "", {
                    "for": `type_${entry["id"]}`
                })
                let order_type = createElement("select", "", lito, `type_${entry["id"]}`, "", {
                    "name": `type_${entry["id"]}`,
                    "disabled": "disabled",
                })
                let order_type_options = createElement("option", entry["target_order_type"], order_type, "", "", {
                    "value": entry["target_order_type"],
                    "selected": "selected"
                })
                if (entry["target_order_type"] !== "Letter") {
                    let order_type_options_1 = createElement("option", "Letter", order_type, "", "", {
                    "value": "Letter",
                    })
                }
                if (entry["target_order_type"] !== "Parcel") {
                    let order_type_options_2 = createElement("option", "Parcel", order_type, "", "", {
                    "value": "Parcel",
                    })
                }
                if (entry["target_order_type"] !== "Box") {
                    let order_type_options_3 = createElement("option", "Box", order_type, "", "", {
                    "value": "Box",
                    })
                }
                let minLabel = createElement("label", "Min Weight", lito, "", "", {
                    "for": `min_w_${entry["id"]}`
                })
                let minInput = createElement("input", `${entry["min_weight"]}`, lito, `min_w_${entry["id"]}`, "", {
                    "name": `min_w_${entry["id"]}`,
                    "type": "number",
                    "onkeypress": "return checkNumber(event)",
                    "value": entry["min_weight"],
                    "disabled": "disabled"
                })
                let maxLabel = createElement("label", "Max Weight", lito, "", "", {
                    "for": `max_w_${entry["id"]}`
                })
                let maxInput = createElement("input", entry["max_weight"], lito, `max_w_${entry["id"]}`, "", {
                    "name": `max_w_${entry["id"]}`,
                    "type": "number",
                    "onkeypress": "return checkNumber(event)",
                    "value": entry["max_weight"],
                    "disabled": "disabled"
                })
                let priceLabel = createElement("label", "Price/kg", lito, "", "", {
                    "for": `price_${entry["id"]}`
                })
                let priceInput = createElement("input", entry["price_per_kg"], lito, `price_${entry["id"]}`, "", {
                    "name": `price_${entry["id"]}`,
                    "type": "number",
                    "value": entry["price_per_kg"],
                    "disabled": "disabled"
                })
                let editBtn = createElement("button", "Edit", lito, entry["id"], ["a_button_inside"])
                editBtn.addEventListener("click", editFunc)
                let removeBtn = createElement("button", "Remove", lito, entry["id"], ["a_button_inside"])
                removeBtn.addEventListener("click", deleteFunc)
            }
        // if initial state = 1 remove the content from target Div and show back the orders div
        } else if (initialState === 1) {
            initialState = 0
            pricesWindow.innerHTML = ''
            pricesWindow.style.display = 'none'
            ordersWindow.style.display = 'grid'
            // Show back the Order Create button and hide the show Orders button
            createOrderBtn.style.display = "block"
            createOrderBtn.hidden = false
            showOrderBtn.style.display = "none"
            showOrderBtn.hidden = true
        }
    }
    // Clear function that defaults the fields of the create form and clears and hides errors
    function clearFunc(e) {
        document.getElementById("min_w_id").value = ""
        document.getElementById("max_w_id").value = ""
        document.getElementById("price_id").value = ""
        document.getElementById("type_id").value = "Letter"
        let error_field = document.getElementById("error_li")
        error_field.style.display = "none"
        error_field.hidden = true
        error_field.textContent = ""
    }
    // Edit function to activate the required fields for editing
    function editFunc(e) {
        // Take the current DB entry
        let currentLi= e.currentTarget.parentNode
        // Take and Delete the Edit and Remove Buttons
        let editBtnToBeDelete = e.currentTarget.parentNode.children[8]
        let removeBtnToBeDelete = e.currentTarget.parentNode.children[9]
        editBtnToBeDelete.remove()
        removeBtnToBeDelete.remove()
        // Disable all other buttons in the target Div
        let currentWindows = currentLi.parentNode.children
        for (let i = 1; i < currentWindows.length; i+=1) {
            if (currentWindows[i]["id"] !== currentLi["id"]) {
                let lastIndex = currentWindows[i].children.length
                if (i === 1) {
                    currentWindows[i].children[lastIndex - 2].disabled = true
                    currentWindows[i].children[lastIndex - 1].disabled = true
                } else {
                    currentWindows[i].children[lastIndex - 2].disabled = true
                    currentWindows[i].children[lastIndex - 1].disabled = true
                }
            }
        }
        // Take the fields for the current DB entry, activate them and save their values in temp_vals
        let range = currentLi.children
        for (let i = 1; i < 9; i += 2) {
            range[i].disabled = false
            range[i].readonly = ""
            temp_vals[i] = range[i].value
        }
        // Create Save and Back buttons and associate the DB entry ID
        let saveBtn = createElement("button", "Save", currentLi, this.id, ["a_button_inside"])
        saveBtn.addEventListener("click", saveFunc)
        let backBtn = createElement("button", "Back", currentLi, this.id, ["a_button_inside"])
        backBtn.addEventListener("click", backFunc)
    }
    // Back function to return to list state without activated fields
    function backFunc(e) {
        // Take the current DB entry row
        let currentLi= e.currentTarget.parentNode
        // Take and Delete the Save and Back Buttons
        let saveBtnToBeDelete = e.currentTarget.parentNode.children[8]
        let backBtnToBeDelete = e.currentTarget.parentNode.children[9]
        saveBtnToBeDelete.remove()
        backBtnToBeDelete.remove()
        // Take the error field from DOM
        let save_error_field = document.getElementById("error_li")
        // Enable all other buttons in the target Div
        let currentWindows = currentLi.parentNode.children
        for (let i = 1; i < currentWindows.length; i+=1) {
            if (currentWindows[i]["id"] !== currentLi["id"]) {
                let lastIndex = currentWindows[i].children.length
                if (i === 1) {
                    currentWindows[i].children[lastIndex - 2].disabled = false
                    currentWindows[i].children[lastIndex - 1].disabled = false
                } else {
                    currentWindows[i].children[lastIndex - 2].disabled = false
                    currentWindows[i].children[lastIndex - 1].disabled = false
                }
            }
        }
        // Take the fields for the current DB entry, deactivate them and restore their values from temp_vals
        let range = currentLi.children
        for (let i = 1; i < 9; i += 2) {
            range[i].disabled = true
            range[i].value = temp_vals[i]
        }
        // Hide, deactivate and clean any errors in the error field
        save_error_field.style.display = "none"
        save_error_field.hidden = true
        save_error_field.textContent = ""
        // Create Edit and Remove buttons and associate the DB entry ID
        let editBtn = createElement("button", "Edit", currentLi, this.id, ["a_button_inside"])
        editBtn.addEventListener("click", editFunc)
        let removeBtn = createElement("button", "Remove", currentLi, this.id, ["a_button_inside"])
        removeBtn.addEventListener("click", deleteFunc)
    }
    // Save Function sending a PUT request to REST API
    async function saveFunc(e) {
        // Take the CSRF Token from the Cookie
        let csrftoken = readCookie("csrftoken")
        // Take the current DB entry row
        let currentLi= e.currentTarget.parentNode
        // Take the values from said Row and the Error Field
        let min_w_val = currentLi.children[3].value
        let max_w_val = currentLi.children[5].value
        let price_val = currentLi.children[7].value
        let type_val = currentLi.children[1].value
        let save_error_field = document.getElementById("error_li")
        // Check if the Fields are filled
        if (min_w_val === "" || max_w_val === "" || price_val === "" || type_val === "") {
            save_error_field.style.display = "block"
            save_error_field.hidden = false
            save_error_field.textContent = "All fields must be filled"
            return
        }
        // Check if the Minimum is larger or Equal to the maximum
        if (Number(min_w_val) >= Number(max_w_val)) {
            save_error_field.style.display = "block"
            save_error_field.hidden = false
            save_error_field.textContent = "minimum value is larger or equal to maximum value"
            return
        }
        // Check for negative Numbers
        if (Number(min_w_val) < 0 || Number(max_w_val) < 0 || Number(price_val) < 0) {
            save_error_field.style.display = "block"
            save_error_field.hidden = false
            save_error_field.textContent = "All values must be greater than 0"
            return
        }
        // create a bool to see if Sequential checks are passed in the for loop
        let checkPassed = true
        // Iterate over each row from the DOM skipping the error and create fields
        let temp_range = this.parentNode.parentNode.children
        for (let i = 2; i < temp_range.length; i++) {
            // Check to skip the row which is currently being saved
            if (currentLi["id"] !== temp_range[i]["id"]) {
                let current_min = temp_range[i].children[3].value
                let current_max = temp_range[i].children[5].value
                // Check to skip the rows with different Price_type
                if (type_val === temp_range[i].children[1].value) {
                    // If both min and max are smaller than the currently checked row min_val just skip the row
                    if (Number(min_w_val) < Number(current_min) && Number(max_w_val) < Number(current_min)) {}
                    // Else if both min and max are bigger than the currently checked row max_val just skip the row
                    else if (Number(min_w_val) > Number(current_max) && Number(max_w_val) > Number(current_max)) {}
                    // If entered_min is bigger then currently checked min and entered_max is smaller than currently checked max
                    // A subrange is detected meaning a put request must be sent to update its min and max values
                    else if (Number(min_w_val) > Number(current_min) && Number(max_w_val) < Number(current_max)) {
                        let res = await fetch(`${window.URLS.prices}${this.id}/`, {
                            method: "PUT",
                            credentials: "same-origin",
                            headers: {
                            "Content-Type": "application/json",
                            "X-CSRFToken":csrftoken,
                            },
                            body: JSON.stringify({
                            "max_weight": max_w_val,
                            'min_weight': min_w_val,
                            'price_per_kg': price_val,
                            "target_order_type": type_val,
                            })
                        })
                        // Changed the state to 0 to allow Prices button to toggle
                        initialState = 0
                        // Invoke the List function to re-list the DB entries again
                        ListPrices(e)
                        // Mark CheckPassed bool as false to prevent creating duplicating entries
                        checkPassed = false
                        // Break the for loop
                        break
                    } else {
                        // If none of the above ifs is entered an overlapping range is detected
                        // meaning the ranges are not sequential and error must be thrown in the error field
                        save_error_field.style.display = "block"
                        save_error_field.hidden = false
                        save_error_field.textContent = "Ranges Must be Sequential"
                        // Mark CheckPassed bool as false to prevent creating overlapping entries
                        checkPassed = false
                        // Break the Loop
                        break
                    }
                }
            }
        }
        // Once all the rows are checked if the bool is still true this means that a new range is detected
        // Meaning that the values of min and max are either higher or lower than all other values in the DB
        if (checkPassed === true) {
            // Send a PUT request to the REST API to create this new range
            let res = await fetch(`${window.URLS.prices}${this.id}/`, {
                method: "PUT",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken":csrftoken,
                },
                body: JSON.stringify({
                    "max_weight": max_w_val,
                    'min_weight': min_w_val,
                    'price_per_kg': price_val,
                    "target_order_type": type_val,
                })
            })
            // Changed the state to 0 to allow Prices button to toggle
            initialState = 0
            // Invoke the List function to re-list the DB entries again
            ListPrices(e)
        }
    }
    // Remove function that sends a delete request once the OK button is pressed
    async function removeFunc(e) {
        // Take the CRSF Token prior of sending the request
        let csrftoken = readCookie("csrftoken")
        let res = await fetch(`${window.URLS.prices}${this.id}/`, {
            method: "DELETE",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken":csrftoken,
            },
        })
        // Changed the state to 0 to allow Prices button to toggle
        initialState = 0
        // Invoke the List function to re-list the DB entries again
        ListPrices(e)
    }
    // Delete Function that changes DOM elements to allow for dialog box prior or deleting an DB entry
    function deleteFunc(e) {
        // Take the current DB entry row from DOM
        let currentLi= e.currentTarget.parentNode
        // Take and Remove the Edit and Remove Buttons
        let editBtnToBeDelete = e.currentTarget.parentNode.children[8]
        let removeBtnToBeDelete = e.currentTarget.parentNode.children[9]
        editBtnToBeDelete.remove()
        removeBtnToBeDelete.remove()
        // Disable all other buttons in the target Div
        let currentWindows = currentLi.parentNode.children
        for (let i = 1; i < currentWindows.length; i+=1) {
            if (currentWindows[i]["id"] !== currentLi["id"]) {
                let lastIndex = currentWindows[i].children.length
                if (i === 1) {
                    currentWindows[i].children[lastIndex - 2].disabled = true
                    currentWindows[i].children[lastIndex - 1].disabled = true
                } else {
                    currentWindows[i].children[lastIndex - 2].disabled = true
                    currentWindows[i].children[lastIndex - 1].disabled = true
                }
            }
        }
        // Take the fields for the current DB entry and save their values in temp_vals
        let range = currentLi.children
        for (let i = 1; i < 9; i += 2) {
            temp_vals[i] = range[i].value
        }
        // Create Delete and Back Buttons
        let delBtn = createElement("button", "OK", currentLi, this.id, ["a_button_inside"])
        delBtn.addEventListener("click", removeFunc)
        let backBtn = createElement("button", "Cancel", currentLi, this.id, ["a_button_inside"])
        backBtn.addEventListener("click", backFunc)
    }
    // Add function that creates a new DB entry sending POST request to REST API
    async function addFunc(e) {
        // Take the CSRF Token
        let csrftoken = readCookie("csrftoken")
        e.preventDefault()
        // Take the values from create fields and the Error Field
        let min_w_val = document.getElementById("min_w_id").value
        let max_w_val = document.getElementById("max_w_id").value
        let price_val = document.getElementById("price_id").value
        let type_val = document.getElementById("type_id").value
        let error_field = document.getElementById("error_li")
        // Check if the Fields are filled
        if (min_w_val === "" || max_w_val === "" || price_val === "" || type_val === "") {
            error_field.style.display = "block"
            error_field.hidden = false
            error_field.textContent = "All fields must be filled"
            return
        }
        // Check if the Minimum is larger or Equal to the maximum
        if (Number(min_w_val) >= Number(max_w_val)) {
            error_field.style.display = "block"
            error_field.hidden = false
            error_field.textContent = "minimum value is larger or equal to maximum value"
            return
        }
        // Check for negative Numbers
        if (Number(min_w_val) < 0 || Number(max_w_val) < 0 || Number(price_val) < 0) {
            error_field.style.display = "block"
            error_field.hidden = false
            error_field.textContent = "All values must be greater than 0"
            return
        }
        // create a bool to see if Sequential checks are passed in the for loop
        let checkPassed = true
        // Iterate over each row from the DOM skipping the error and create fields
        let range = this.parentNode.parentNode.children
        for (let i = 2; i < range.length; i++) {
            let current_min = range[i].children[3].value
            let current_max = range[i].children[5].value
            if (type_val === range[i].children[1].value) {
                // If both min and max are smaller than the currently checked row min_val just skip the row
                if (Number(min_w_val) < Number(current_min) && Number(max_w_val) < Number(current_min)) {}
                // Else if both min and max are bigger than the currently checked row max_val just skip the row
                else if (Number(min_w_val) > Number(current_max) && Number(max_w_val) > Number(current_max)) {}
                // If entered_min is bigger then currently checked min and entered_max is smaller than currently checked max
                // A subrange is detected meaning a put request must be sent to update its min and max values
                else if (Number(min_w_val) > Number(current_min) && Number(max_w_val) < Number(current_max)) {
                    // Subrange detected must trow error for create but not for edit
                    error_field.style.display = "block"
                    error_field.hidden = false
                    error_field.textContent = "Current Range is a Sub-Range of Another Entry"
                    // Mark CheckPassed bool as false to prevent creating overlapping entries
                    checkPassed = false
                    // Break the Loop
                    break
                }
                else {
                    // If none of the above ifs is entered an overlapping range is detected
                    // Meaning the ranges are not sequential and error must be thrown in the error field
                    error_field.style.display = "block"
                    error_field.hidden = false
                    error_field.textContent = "Ranges Must be Sequential"
                    // Mark CheckPassed bool as false to prevent creating overlapping entries
                    checkPassed = false
                    // Break the Loop
                    break
                }
            }
        }
        // Once all the rows are checked if the bool is still true this means that a new range is detected
        // Meaning that the values of min and max are either higher or lower than all other values in the DB
        if (checkPassed === true) {
            let res = await fetch(window.URLS.prices, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken":csrftoken,
                },
                body: JSON.stringify({
                    "max_weight": max_w_val,
                    'min_weight': min_w_val,
                    'price_per_kg': price_val,
                    "target_order_type": type_val,
                })
            })
            // Changed the state to 0 to allow Prices button to toggle
            initialState = 0
            // Invoke the List function to re-list the DB entries again
            ListPrices(e)
        }
    }
    // ------ Helper Functions ------
    // Read Cookie function that takes parses the cookie and takes the CSRF token from it
    function readCookie(name) {
        let nameEQ = name + "=";
        let ca = document.cookie.split(';');
        for(let i=0;i < ca.length;i++) {
            let c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1,c.length);
            if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
        }
        return null;
    }
    // Create HTML elements function that helps create, fill, attach, and specify HTML elements
    function createElement(type, content, parentNode, id, classes, attributes) {
        const htmlElement = document.createElement(type);
        if (content && (type !== "input" && type !== "textarea")) {
          htmlElement.textContent = content;
        }
        if (content && (type === "input" || type === "textarea")) {
          htmlElement.value = content;
        }
        if (id) {
          htmlElement.id = id;
        }
        if (classes) {
          htmlElement.classList.add(...classes);
        }
        if (attributes) {
          for (const key in attributes) {
            htmlElement.setAttribute(key, attributes[key]);
          }
        }
        if (parentNode) {
          parentNode.appendChild(htmlElement);
        }
        return htmlElement;
    }
}