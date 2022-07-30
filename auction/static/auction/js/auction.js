function HighOfferToBuy() {
    let offer = {
        HighBuyMarketPrice : document.getElementById("HighBuyMarketPrice").value,
        HighBuyMarketQuantity : document.getElementById("HighBuyMarketQuantity").value
    }
    liveSend(offer)
}

function HighOfferToSell() {
    let offer = {
        HighSellMarketPrice : document.getElementById("HighSellMarketPrice").value,
        HighSellMarketQuantity : document.getElementById("HighSellMarketQuantity").value
    }
    liveSend(offer)
}

function LowOfferToBuy() {
    let offer = {
        LowBuyMarketPrice : document.getElementById("LowBuyMarketPrice").value,
        LowBuyMarketQuantity : document.getElementById("LowBuyMarketQuantity").value
    }
    liveSend(offer)
}

function LowOfferToSell() {
    let offer = {
        LowSellMarketPrice : document.getElementById("LowSellMarketPrice").value,
        LowSellMarketQuantity : document.getElementById("LowSellMarketQuantity").value
    }
    liveSend(offer)
}

function liveRecv(data) {
    history.innerHTML += '<tr><td>' + data.id_in_group + '</td><td>' + data.bid + '</td></tr>';
}