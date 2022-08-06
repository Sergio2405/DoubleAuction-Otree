function HighOfferToBuy() {
    let offer = {
        Asset : "High",
        Type : "Limit",
        Action : "Buy",
        Price : parseFloat(document.getElementById("HighBuyLimitPrice").value),
        Quantity : parseInt(document.getElementById("HighBuyLimitQuantity").value)
    }
    liveSend(offer)
}

function HighOfferToSell() {
    let offer = {
        Asset : "High",
        Type : "Limit",
        Action : "Sell",
        Price : parseFloat(document.getElementById("HighSellLimitPrice").value),
        Quantity : parseInt(document.getElementById("HighSellLimitQuantity").value)
    }
    liveSend(offer)
}

function LowOfferToBuy() {
    let offer = {
        Asset : "Low",
        Type : "Limit",
        Action : "Buy",
        Price : parseFloat(document.getElementById("LowBuyLimitPrice").value),
        Quantity : parseInt(document.getElementById("LowBuyLimitQuantity").value)
    }
    liveSend(offer)
}

function LowOfferToSell() {
    let offer = {
        Asset : "Low",
        Type : "Limit",
        Action : "Sell",
        Price : parseFloat(document.getElementById("LowSellLimitPrice").value),
        Quantity : parseInt(document.getElementById("LowSellLimitQuantity").value)
    }
    liveSend(offer)
}

function HighSell() {
    let offer = {
        Asset : "High",
        Type : "Market",
        Action : "Sell",
        Quantity : parseInt(document.getElementById("HighSellMarket").value)
    }
    liveSend(offer)
}

function HighBuy() {
    let offer = {
        Asset : "High",
        Type : "Market",
        Action : "Buy",
        Quantity : parseInt(document.getElementById("HighBuyMarket").value)
    }
    liveSend(offer)
}

function LowSell() {
    let offer = {
        Asset : "Low",
        Type : "Market",
        Action : "Sell",
        Quantity : parseInt(document.getElementById("LowSellMarket").value)
    }
    liveSend(offer)
}

function LowBuy() {
    let offer = {
        Asset : "Low",
        Type : "Market",
        Action : "Buy",
        Quantity : parseInt(document.getElementById("LowBuyMarket").value)
    }
    liveSend(offer)
}

function liveRecv(data) {

    let high_risk_orders = data["high_risk_orders"];
    let low_risk_orders = data["low_risk_orders"];

    let players = data["players"];
    let my_player;

    console.log(players)
    console.log(player_id)
    
    for (let player of players) { 
        if (player.player_id == player_id){ 
            my_player = player
            break
        }
    }

    let holdings = my_player["holdings"];
    let quantity = my_player["quantity"];
    let orders_issued = my_player["orders"];

    document.getElementById("HighRiskHoldings").innerHTML = '<tr><td>High Risk</td><td>' +  quantity.high_risk + '</td></tr>';
    document.getElementById("LowRiskHoldings").innerHTML = '<tr><td>Low Risk</td><td>' + quantity.low_risk + '</td></tr>';
    document.getElementById("TotalHoldings").innerHTML = 'Capital =  '  + '<strong>' + holdings.total + ' Puntos</strong>'

    document.getElementById("HighBuyTable").innerHTML = ""
    document.getElementById("HighSellTable").innerHTML = ""
    document.getElementById("LowBuyTable").innerHTML = ""
    document.getElementById("LowSellTable").innerHTML = ""

    document.getElementById("HighBuyMyOffersTable").innerHTML = ""
    document.getElementById("HighSellMyOffersTable").innerHTML = ""
    document.getElementById("LowBuyMyOffersTable").innerHTML = ""
    document.getElementById("LowSellMyOffersTable").innerHTML = ""

    for (let order of orders_issued) { 
        if (order.Asset == "High"){ 
            let buy_orders_table1 = document.getElementById("HighBuyMyOffersTable");
            let sell_orders_table1 = document.getElementById("HighSellMyOffersTable");

            if (order.Action == "Sell") { 
                sell_orders_table1.innerHTML += '<tr><td>' + order.Price + '</td><td>' + order.Quantity + '</td></tr>'
            } else { 
                buy_orders_table1.innerHTML += '<tr><td>' + order.Price + '</td><td>' + order.Quantity + '</td></tr>'
            }
        }else{
            let buy_orders_table = document.getElementById("LowBuyMyOffersTable");
            let sell_orders_table = document.getElementById("LowSellMyOffersTable");

            if (order.Action == "Sell") { 
                sell_orders_table.innerHTML += '<tr><td>' + order.Price + '</td><td>' + order.Quantity + '</td></tr>'
            } else { 
                buy_orders_table.innerHTML += '<tr><td>' + order.Price + '</td><td>' + order.Quantity + '</td></tr>'
            }
        }
    }

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
