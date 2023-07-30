function showFunc() {
    let createOrderBtn = document.getElementById("create-order-btn")
    let showOrderBtn = document.getElementById("show-order-btn")
    let discountWindow = document.getElementById("discount-window")
    let pricesWindow = document.getElementById("prices-window")
    let ordersWindow = document.getElementById("orders-window")
    initialState = 0
    initialState2 = 0
    discountWindow.innerHTML = ''
    ordersWindow.style.display = 'flex'
    pricesWindow.innerHTML = ""
    createOrderBtn.style.display = "block"
    createOrderBtn.hidden = false
    showOrderBtn.style.display = "none"
    showOrderBtn.hidden = true
}