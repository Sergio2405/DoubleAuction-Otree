function validation(price, quantity) {
    return ((price > 0) && (quantity >0))
}

function HighOfferToBuy() {
    
    let holdings = parseFloat(document.getElementById("HighHoldings").value);

    let price = parseFloat(document.getElementById("HighBuyLimitPrice").value);
    price = Math.round(price * 100) / 100;
    
    let quantity = parseInt(document.getElementById("HighBuyLimitQuantity").value)

    if (validation(price,quantity)){
        let offer = {
            Asset : "High",
            Type : "Limit",
            Action : "Buy",
            Price : price,
            Quantity : quantity
        }

        let amount = price * quantity;
        console.log(holdings)
        if (amount > holdings){
            alert(`
                \t NO PROCEDE LA OFERTA DE COMPRA \t \n
                Nota: \t
                • Ofreces pagar un precio: ${price} por una cantidad: ${quantity} 
                • lo cual supera tu actual presupuesto de: ${holdings} 
            `)
        }else{
            liveSend(offer)
        }
    }else {
        alert(`
                \t VALORES INGRESADOS NO VÁLIDOS \t \n
                Nota: \t
                • El Precio o la Cantidad es negativo o igual a 0
            `)
    }
}

function HighOfferToSell() {

    let high_risk_quantity = parseInt(document.getElementById("High").value);

    let price = parseFloat(document.getElementById("HighSellLimitPrice").value);
    price = Math.round(price * 100) / 100;

    let quantity = parseInt(document.getElementById("HighSellLimitQuantity").value)

    if (validation(price,quantity)){

        let offer = {
            Asset : "High",
            Type : "Limit",
            Action : "Sell",
            Price : price,
            Quantity : quantity
        }
      
        if ((quantity > high_risk_quantity)){
            alert(`
                \t NO PROCEDE LA OFERTA DE VENTA \t \n
                Nota: \t
                • Ofreces vender una cantidad: ${quantity} 
                • la cual supera la cantidad que tienes de este activo: ${high_risk_quantity} 
            `)
        }else{
            liveSend(offer)
        }
    }else {
        alert(`
                \t VALORES INGRESADOS NO VÁLIDOS \t \n
                Nota: \t
                • El Precio o la Cantidad es negativo o igual a 0
            `)
    }
}

function LowOfferToBuy() {

    let holdings = parseFloat(document.getElementById("LowHoldings").value);

    let price = parseFloat(document.getElementById("LowBuyLimitPrice").value);
    price = Math.round(price * 100) / 100;

    let quantity = parseInt(document.getElementById("LowBuyLimitQuantity").value)

    if (validation(price,quantity)) {

        let offer = {
            Asset : "Low",
            Type : "Limit",
            Action : "Buy",
            Price : price,
            Quantity : quantity
        }
    
        let amount = price * quantity;
    
        if (amount > holdings){
            alert(`
                \t NO PROCEDE LA OFERTA DE COMPRA \t \n
                Nota: \t
                • Ofreces pagar un precio: ${price} por una cantidad: ${quantity} 
                • lo cual supera tu actual presupuesto de: ${holdings} 
            `)
        }else{
            liveSend(offer)
        }
    }else {
        alert(`
                \t VALORES INGRESADOS NO VÁLIDOS \t \n
                Nota: \t
                • El Precio o la Cantidad es negativo o igual a 0
            `)
    }

}

function LowOfferToSell() {

    let low_risk_quantity = parseInt(document.getElementById("Low").value);

    let price = parseFloat(document.getElementById("LowSellLimitPrice").value);
    price = Math.round(price * 100) / 100;

    let quantity = parseInt(document.getElementById("LowSellLimitQuantity").value)
    
    if (validation(price,quantity)){

        let offer = {
                Asset : "Low",
                Type : "Limit",
                Action : "Sell",
                Price : price,
                Quantity : quantity
            }

        if ((quantity > low_risk_quantity)){
            alert(`
                \t NO PROCEDE LA OFERTA DE VENTA \t \n
                Nota: \t
                • Ofreces vender una cantidad: ${quantity} 
                • la cual supera la cantidad que tienes de este activo: ${low_risk_quantity} 
            `)
        }else{
            liveSend(offer)
        }
    }else {
        alert(`
                \t VALORES INGRESADOS NO VÁLIDOS \t \n
                Nota: \t
                • El Precio o la Cantidad es negativo o igual a 0
            `)
    }

    
}

function HighSell() {

    let high_risk_quantity = parseInt(document.getElementById("High").value);

    let quantity = parseInt(document.getElementById("HighSellMarket").value)


    if (quantity > 0) {

        let offer = {
            Asset : "High",
            Type : "Market",
            Action : "Sell",
            Quantity : quantity
        }
    
        if ((quantity > high_risk_quantity)){
            alert(`
                \t NO PROCEDE LA OFERTA DE VENTA \t \n
                Nota: \t
                • Ofreces vender una cantidad: ${quantity} 
                • la cual supera la cantidad que tienes de este activo: ${high_risk_quantity} 
            `)
        }else{
            liveSend(offer)
        }
    }else {
        alert(`
                \t VALORES INGRESADOS NO VÁLIDOS \t \n
                Nota: \t
                • El Precio debe ser mayor que 0
            `)
    }
}

function HighBuy() {

    let holdings = parseFloat(document.getElementById("HighHoldings").value);

    let price = parseFloat(document.getElementById("HighPrice").value);
    price = Math.round(price * 100) / 100;

    let quantity = parseInt(document.getElementById("HighBuyMarket").value)

    if (quantity > 0) {

        let offer = {
            Asset : "High",
            Type : "Market",
            Action : "Buy",
            Quantity : quantity
        }
    
        let amount = price * quantity;
    
        if (amount > holdings){
            alert(`
                \t NO PROCEDE LA OFERTA DE COMPRA \t \n
                Nota: \t
                • El precio promedio del activo es: ${price} y ofreces comprar una cantidad: ${quantity} 
                • lo cual supera tu actual presupuesto de: ${holdings} 
            `)
        }else{
            liveSend(offer)
        }
    }else {
        alert(`
                \t VALORES INGRESADOS NO VÁLIDOS \t \n
                Nota: \t
                • El Precio debe ser mayor que 0
            `)
    }
}

function LowSell() {

    let low_risk_quantity = parseInt(document.getElementById("Low").value);

    let quantity = parseInt(document.getElementById("LowSellMarket").value)

    if (quantity > 0) { 

        let offer = {
            Asset : "Low",
            Type : "Market",
            Action : "Sell",
            Quantity : quantity
        }
    
        if ((quantity > low_risk_quantity)){
            alert(`
                \t NO PROCEDE LA OFERTA DE VENTA \t \n
                Nota: \t
                • Ofreces vender una cantidad: ${quantity} 
                • la cual supera la cantidad que tienes de este activo: ${low_risk_quantity} 
            `)
        }else{
            liveSend(offer)
        }
    }else {
        alert(`
                \t VALORES INGRESADOS NO VÁLIDOS \t \n
                Nota: \t
                • El Precio debe ser mayor que 0
            `)
    }
}

function LowBuy() {

    let holdings = parseInt(document.getElementById("LowHoldings").value);

    let price = parseFloat(document.getElementById("LowPrice").value);
    price = Math.round(price * 100) / 100;

    let quantity = parseInt(document.getElementById("LowBuyMarket").value);

    if (quantity > 0) {

        let offer = {
            Asset : "Low",
            Type : "Market",
            Action : "Buy",
            Quantity : quantity
        }
    
        let amount = price * quantity;
    
        if (amount > holdings){
            alert(`
                \t NO PROCEDE LA OFERTA DE COMPRA \t \n
                Nota: \t
                • El precio promedio del activo es: ${price} y ofreces comprar una cantidad: ${quantity} 
                • lo cual supera tu actual presupuesto de: ${holdings} 
            `)
        }else{
            liveSend(offer)
        }
    }else {
        alert(`
                \t VALORES INGRESADOS NO VÁLIDOS \t \n
                Nota: \t
                • El Precio debe ser mayor que 0
            `)
    }
}

function liveRecv(data) {
    
    let high_risk_orders = data["high_risk_orders"];
    let low_risk_orders = data["low_risk_orders"];

    let players = data["players"];
    let my_player;
    
    for (let player of players) { 
        if (player.player_id == player_id){ 
            my_player = player
            break
        }
    }

    let holdings = my_player["holdings"];
    let quantity = my_player["quantity"];
    let prices = my_player["prices"];
    
    let high_price = Math.round(prices["high"] * 100) / 100;
    let low_price = Math.round(prices["low"] * 100) / 100;


    document.getElementById("HighRiskHoldings").innerHTML = '<tr><td>High Risk</td><td>' +  quantity.high_risk + '</td><td>'+ holdings.high_risk +'</td></tr>';
    document.getElementById("LowRiskHoldings").innerHTML = '<tr><td>Low Risk</td><td>' + quantity.low_risk + '</td><td>'+ holdings.low_risk +'</td></tr>';

    document.getElementById("TotalHoldings").innerHTML = 'Capital Total =  '  + '<strong>' + holdings.total + ' Puntos</strong>';

    document.getElementById("AssetPrices").innerHTML = `<td>${high_price}</td><td>${low_price}</td>`;
    document.getElementById("HighPrice").value = high_price
    document.getElementById("LowPrice").value = low_price

    document.getElementById("Total").value = holdings.total;

    document.getElementById("Low").value = quantity.low_risk;
    document.getElementById("LowHoldings").value = holdings.low_risk;

    document.getElementById("High").value = quantity.high_risk;
    document.getElementById("HighHoldings").value = holdings.high_risk;


    document.getElementById("HighBuyTable").innerHTML = ""
    document.getElementById("HighSellTable").innerHTML = ""
    document.getElementById("LowBuyTable").innerHTML = ""
    document.getElementById("LowSellTable").innerHTML = ""

    for (let order of high_risk_orders) { 

        let color_order = order.player_id == player_id ? "#bbbbfc" : "#ababad";

        let buy_orders_table = document.getElementById("HighBuyTable");
        let sell_orders_table = document.getElementById("HighSellTable");

        if (order.Action == "Sell") { 
            sell_orders_table.innerHTML += `<tr style = "background-color:${color_order}"><td>${order.Price}</td><td>${order.Quantity}</td></tr>`
        } else { 
            buy_orders_table.innerHTML += `<tr style = "background-color:${color_order}"><td>${order.Price}</td><td>${order.Quantity}</td></tr>`
        }
    }

    for (order of low_risk_orders) { 

        let color_order = order.player_id == player_id ? "#bbbbfc" : "#ababad";

        let buy_orders_table = document.getElementById("LowBuyTable");
        let sell_orders_table = document.getElementById("LowSellTable");

        if (order.Action == "Sell") { 
            sell_orders_table.innerHTML += `<tr style = "background-color:${color_order}"><td>${order.Price}</td><td>${order.Quantity}</td></tr>`
        } else { 
            buy_orders_table.innerHTML += `<tr style = "background-color:${color_order}"><td>${order.Price}</td><td>${order.Quantity}</td></tr>`
        }
    }
}

window.onload = function () { 
    liveSend({'Type': 'Connect'})
}
