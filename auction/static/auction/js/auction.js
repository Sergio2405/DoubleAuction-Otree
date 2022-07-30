function HighOfferToBuy() {
    let offer = {
        Asset : "High",
        Type : "Limit",
        Action : "Buy",
        Price : document.getElementById("HighBuyLimitPrice").value,
        Quantity : document.getElementById("HighBuyLimitQuantity").value
    }
    liveSend(offer)
}

function HighOfferToSell() {
    let offer = {
        Asset : "High",
        Type : "Limit",
        Action : "Sell",
        Price : document.getElementById("HighSellLimitPrice").value,
        Quantity : document.getElementById("HighSellLimitQuantity").value
    }
    liveSend(offer)
}

function LowOfferToBuy() {
    let offer = {
        Asset : "Low",
        Type : "Limit",
        Action : "Buy",
        Price : document.getElementById("LowBuyLimitPrice").value,
        Quantity : document.getElementById("LowBuyLimitQuantity").value
    }
    liveSend(offer)
}

function LowOfferToSell() {
    let offer = {
        Asset : "Low",
        Type : "Limit",
        Action : "Sell",
        Price : document.getElementById("LowSellLimitPrice").value,
        Quantity : document.getElementById("LowSellLimitQuantity").value
    }
    liveSend(offer)
}

function HighSell() {
    let offer = {
        Asset : "High",
        Type : "Market",
        Action : "Sell",
        Quantity : document.getElementById("HighSellMarket").value
    }
    liveSend(offer)
}

function HighBuy() {
    let offer = {
        Asset : "High",
        Type : "Market",
        Action : "Buy",
        Quantity : document.getElementById("HighBuyMarket").value
    }
    liveSend(offer)
}

function LowSell() {
    let offer = {
        Asset : "Low",
        Type : "Market",
        Action : "Sell",
        Quantity : document.getElementById("LowSellMarket").value
    }
    liveSend(offer)
}

function LowBuy() {
    let offer = {
        Asset : "Low",
        Type : "Market",
        Action : "Buy",
        Quantity : document.getElementById("LowBuyMarket").value
    }
    liveSend(offer)
}

function liveRecv(data) {

    let high_risk_orders = data["high_risk_orders"];
    let low_risk_orders = data["low_risk_orders"];

    document.getElementById("HighBuyTable").innerHTML = ""
    document.getElementById("HighSellTable").innerHTML = ""
    document.getElementById("LowBuyTable").innerHTML = ""
    document.getElementById("LowSellTable").innerHTML = ""

    for (let order of high_risk_orders) { 

        let buy_orders_table = document.getElementById("HighBuyTable");
        let sell_orders_table = document.getElementById("HighSellTable");

        if (order.Action == "Sell") { 
            sell_orders_table.innerHTML += '<tr><td>' + order.Price + '</td><td>' + order.Quantity + '</td></tr>'
        } else { 
            buy_orders_table.innerHTML += '<tr><td>' + order.Price + '</td><td>' + order.Quantity + '</td></tr>'
        }
    }

    for (order of low_risk_orders) { 

        let buy_orders_table = document.getElementById("LowBuyTable");
        let sell_orders_table = document.getElementById("LowSellTable");

        if (order.Action == "Sell") { 
            sell_orders_table.innerHTML += '<tr><td>' + order.Price + '</td><td>' + order.Quantity + '</td></tr>'
        } else { 
            buy_orders_table.innerHTML += '<tr><td>' + order.Price + '</td><td>' + order.Quantity + '</td></tr>'
        }
    }
}

window.onload = function () { 
    liveSend({'Type': 'Connect'})
}