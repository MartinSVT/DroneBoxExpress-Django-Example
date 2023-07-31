window.addEventListener('load', calcFunc);

function calcFunc() {
    let calculateBtn = document.getElementById("calc_btn")
    calculateBtn.addEventListener("click", priceCalculator)
    let iniWeight = document.getElementById("id_weight")
    let iniOrderType = document.getElementById("id_order_type")
    let iniRouteId = document.getElementById("id_order_route")
    iniWeight.addEventListener("change", disableSubmit)
    iniOrderType.addEventListener("change", disableSubmit)
    iniRouteId.addEventListener("change", disableSubmit)
    let submitBtn = document.getElementById("order-submit-btn")
    submitBtn.disabled = true
    submitBtn.style.backgroundColor = "grey"

    function disableSubmit(e) {
        let submitBtn = document.getElementById("order-submit-btn")
        submitBtn.disabled = true
        submitBtn.style.backgroundColor = "grey"
    }

    async function priceCalculator(e) {
        e.preventDefault()
        let costFiled = document.getElementById("id_cost")
        let errorField = document.getElementById("errors_p")
        let weight = document.getElementById("id_weight").value
        let orderType = document.getElementById("id_order_type").value
        let routeId = document.getElementById("id_order_route").value
        let currentRevenue = JSON.parse(document.getElementById('revenue').textContent);
        let profileType = JSON.parse(document.getElementById('profile_type').textContent);
        // Check the inputs for missing fields
        if (weight === "" || routeId === "" || orderType === "") {
            errorField.style.display = "block"
            errorField.hidden = false
            errorField.textContent = "All fields must be filled"
            return
        }
        // Check that weight is between 0 and 50
        if (Number(weight) > 50 || Number(weight) < 0) {
            errorField.style.display = "block"
            errorField.hidden = false
            errorField.textContent = "Weight must be between 0 and 50"
            return
        }
        // Take the prices via POST request to Django REST
        let prices = await fetch(window.URLS.prices)
        let pricesData = await prices.json()
        // Filler the data so that only prices for that particular order type are left
        let relevantPricesData = [];
        for (let tempEntry of pricesData.values()) {
            if (orderType === tempEntry["target_order_type"]) {
                relevantPricesData.push(tempEntry)
            }
        }
        // If no prices exist trow error that this order type is not available
        if (relevantPricesData.length === 0) {
            errorField.style.display = "block"
            errorField.hidden = false
            errorField.textContent = "This order type is currently not available"
            return
        }
        // Sort the prices by weight value starting from the minimum
        let pricesSortedValues = relevantPricesData.sort(function (a, b) {
            return a.min_weight - b.max_weight})
        // Take the minimum and maximum entries from the price ranges in sorted prices data
        let minimumWeightEntry = pricesSortedValues[0]
        let maximumWeightEntry = pricesSortedValues[pricesSortedValues.length - 1]
        // Check if the selected weight is outside the available weight ranges is so set min or max
        let currentPricePerKg = 0
        if (Number(weight) < minimumWeightEntry["min_weight"]) {
            // Selected Weight smaller than the minimum weight range minimum price applies
            currentPricePerKg = minimumWeightEntry["price_per_kg"]
        } else if (Number(weight) > maximumWeightEntry["max_weight"]) {
            // Selected Weight bigger than the maximum weight range maximum price applies
            currentPricePerKg = maximumWeightEntry["price_per_kg"]
        } else {
            // else iterate over the PriceModel entries
            for (let entry of pricesSortedValues) {
                // if the selected weight is within a current entry range set its price value
                if (Number(weight) >= entry["min_weight"] && Number(weight) <= entry["max_weight"]){
                    currentPricePerKg = entry["price_per_kg"]
                }
            }
            // else the selected weight is in a gap between the ranges, hence select maximum price
            if (currentPricePerKg === 0) {
                // Selected Weight not within price ranges maximum price applies
                currentPricePerKg = maximumWeightEntry["price_per_kg"]
            }
        }
        // Take the discounts via POST request to Django REST
        let discounts = await fetch(window.URLS.discounts)
        let discountsData = await discounts.json()
        // Filler the data so that only discounts for that particular profile type are left
        let relevantDiscountData = [];
        for (let tempEntryDiscount of discountsData.values()) {
            if (profileType === tempEntryDiscount["discount_profile_type"]) {
                relevantDiscountData.push(tempEntryDiscount)
            }
        }
        let currentDiscount = 0
        // If no discounts exist set discounts to 0
        if (relevantDiscountData.length === 0) {
            currentDiscount = 0
        } else {
            // Sort the discounts by revenue value starting from the minimum
            let discountSortedValues = relevantDiscountData.sort(function (a, b) {
                return a.min_profile_revenue - b.max_profile_revenue})
            // Take the minimum and maximum entries from the discounts ranges in sorted discount data
            let minimumRevenueEntry = discountSortedValues[0]
            let maximumRevenueEntry = discountSortedValues[discountSortedValues.length - 1]
            // Check if the profile revenue is outside the available revenue ranges
            if (Number(currentRevenue) < minimumRevenueEntry["min_profile_revenue"]) {
                // Profile revenue is smaller than the minimum revenue range discount goes to 0
                currentDiscount = 0
            } else if (Number(currentRevenue) > maximumRevenueEntry["max_profile_revenue"]) {
                // Profile revenue is bigger than the maximum revenue range maximum discount applies
                currentDiscount = maximumRevenueEntry["discount_rate"]
            } else {
                // else iterate over the DiscountModel entries
                for (let entryD of discountSortedValues) {
                    // if the profile revenue is within a current entry range set its discount value
                    if (Number(currentRevenue) >= entryD["min_profile_revenue"] && Number(currentRevenue) <= entryD["max_profile_revenue"]){
                        currentDiscount = entryD["discount_rate"]
                    }
                }
                // else the profile revenue is in a gap between the ranges, hence select minimum discount
                if (currentDiscount === 0) {
                    currentDiscount = minimumRevenueEntry["discount_rate"]
                }
            }
        }
        let slicedURL = window.URLS.route.slice(0,-2);
        let routeData = await fetch(`${slicedURL}${routeId}/`)
        let routeDistance = await routeData.json()
        let currentDistance = routeDistance["distance"]
        let cost = (currentDistance * (currentPricePerKg * Number(weight))) * (1 - currentDiscount)
        costFiled.value = cost.toFixed(2)
        costFiled.setAttribute("value", cost.toFixed(2))
        let submitBtn = document.getElementById("order-submit-btn")
        submitBtn.disabled = false
        submitBtn.style.backgroundColor = "cornflowerblue"
    }
}