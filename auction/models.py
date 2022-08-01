from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

import ast

author = 'Sergio Gonzalo Mejia Ramos'

doc = """

Double Auction Market with 2 Assets to trade

"""

class Constants(BaseConstants):
    name_in_url = 'auction'
    players_per_group = None
    num_rounds = 1
    
class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    
    high_risk_orders = models.LongStringField(default = "")
    low_risk_orders = models.LongStringField(default = "")

class Player(BasePlayer):

    high_risk_quantity = models.IntegerField(default = 0)
    high_risk_holdings = models.FloatField(default = 0)

    low_risk_quantity = models.IntegerField(default = 0)
    low_risk_holdings = models.FloatField(default = 0)
    
    def live_auction(self, data):

        data["player_id"] = self.id_in_group
    
        if data["Type"] == "Limit":

            if data["Asset"] == "High": 
                self.group.high_risk_orders += str(data) + "-"
            else: 
                self.group.low_risk_orders += str(data) + "-"
    
        # cualquier operacion que se quiera realizar con las ordenes se hace a partir del mapeo
        high_risk_orders = list(map(lambda order: ast.literal_eval(order),self.group.high_risk_orders.split("-")[:-1]))
        low_risk_orders = list(map(lambda order: ast.literal_eval(order),self.group.low_risk_orders.split("-")[:-1]))

        if data["Type"] == "Market": 

            if data["Asset"] == "High": 

                high_risk_orders_rest = filter(lambda order: order["player_id"] != self.id_in_group ,high_risk_orders)

                if data["Action"] == "Buy":

                    high_risk_sell_offers = filter(lambda order: order["Action"] == "Sell", high_risk_orders_rest)

                    high_risk_best_sell_offer = sorted(high_risk_sell_offers, key = lambda order: order["Price"])[0]

                    quantity_to_buy = data["Quantity"] if data["Quantity"] <= high_risk_best_sell_offer["Quantity"] else high_risk_best_sell_offer["Quantity"]

                    self.high_risk_quantity += quantity_to_buy 
                    self.high_risk_holdings -= quantity_to_buy * high_risk_best_sell_offer["Price"]

                    #delete offer from high_risk_orders
                    high_risk_orders.remove(high_risk_best_sell_offer)

                else: 

                    high_risk_buy_offers = filter(lambda order: order["Action"] == "Buy", high_risk_orders_rest)

                    high_risk_best_buy_offer = sorted(high_risk_buy_offers, key = lambda order: order["Price"])[-1]

                    quantity_to_sell = data["Quantity"] if data["Quantity"] <= high_risk_best_buy_offer["Quantity"] else high_risk_best_buy_offer["Quantity"]

                    self.high_risk_quantity -= quantity_to_sell 
                    self.high_risk_holdings += quantity_to_sell * high_risk_best_buy_offer["Price"]

                    high_risk_orders.remove(high_risk_best_buy_offer)

            if data["Asset"] == "Low": 

                low_risk_orders_rest = filter(lambda order: order["player_id"] != self.id_in_group ,low_risk_orders)

                if data["Action"] == "Buy":

                    low_risk_sell_offers = filter(lambda order: order["Action"] == "Sell", low_risk_orders_rest)

                    low_risk_best_sell_offer = sorted(low_risk_sell_offers, key = lambda order: order["Price"])[0]

                    quantity_to_buy = data["Quantity"] if data["Quantity"] <= low_risk_best_sell_offer["Quantity"] else low_risk_best_sell_offer["Quantity"]

                    self.low_risk_quantity += quantity_to_buy 
                    self.low_risk_holdings -= quantity_to_buy * low_risk_best_sell_offer["Price"]

                    #delete offer from high_risk_orders
                    low_risk_orders.remove(low_risk_best_sell_offer)

                else: 

                    low_risk_buy_offers = filter(lambda order: order["Action"] == "Buy", low_risk_orders_rest)

                    low_risk_best_buy_offer = sorted(low_risk_buy_offers, key = lambda order: order["Price"])[-1]

                    quantity_to_sell = data["Quantity"] if data["Quantity"] <= low_risk_best_buy_offer["Quantity"] else low_risk_best_buy_offer["Quantity"]

                    self.low_risk_quantity -= quantity_to_sell 
                    self.low_risk_holdings += quantity_to_sell * low_risk_best_buy_offer["Price"]

                    low_risk_orders.remove(low_risk_best_buy_offer)

        response = {0:{
            "high_risk_orders" : high_risk_orders,
            "low_risk_orders" : low_risk_orders
        }}

        # updating the orders "database"
        if high_risk_orders: 
            self.group.high_risk_orders = "-".join(list(map(lambda order: str(order),high_risk_orders))) + "-"
        if low_risk_orders: 
            self.group.low_risk_orders = "-".join(list(map(lambda order: str(order),low_risk_orders))) + "-"

        print(response)

        return response
