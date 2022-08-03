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
    num_rounds = 6

    time_per_round = 2 # time in minutes

    endowment = 4000 # points
    initial_quantity = 200 # total initial asset units
    
    treatments = ["AB","TB1","TB2","AP","TP1","TP2"]

class Subsession(BaseSubsession):
    
    def creating_session(self):
      
        group = self.get_groups()[0]
        group.treatment = Constants.treatments[self.round_number-1]
        print(group.treatment)

class Group(BaseGroup):

    treatment = models.StringField(default = "")
    
    # vars usadas como almacenadores de ordenes temporales (vars auxiliares)
    high_risk_orders = models.LongStringField(default = "")
    low_risk_orders = models.LongStringField(default = "")

    # variables de interes 

    # cantidad de ordenes segun tipo
    limit_orders = models.IntegerField(default = 0) # num de limit orders
    market_orders = models.IntegerField(default = 0) # num de market orders

    # guardando las ordenes segun tipo
    high_risk_limit_orders = models.LongStringField(default = "")
    high_risk_market_orders = models.LongStringField(default = "")

    low_risk_limit_orders = models.LongStringField(default = "")
    low_risk_market_orders = models.LongStringField(default = "")

    def get_players_parser(self):
        
        players = self.get_players()
        players_parsed = []
        
        for player in players: 

            player_dict = {
                "player_id" : player.id_in_group,
                "holdings" : {
                        "total" : player.total_holdings,
                        "high_risk" : player.high_risk_holdings,
                        "low_risk" : player.low_risk_holdings
                    },
                "quantity" : {
                        "total" : player.total_quantity,
                        "high_risk" : player.high_risk_quantity,
                        "low_risk" : player.low_risk_quantity
                    },
                "orders" : player.parse_orders()
                }

            players_parsed.append(player_dict)
            print(players_parsed)
        
        return players_parsed

    def get_order_issuer(self,order): 

        players = self.get_players()
        issuer_id = order["player_id"] 
        issuer = None

        for player in players: 
            if player.id_in_group == issuer_id:
                issuer = player
                break

        return issuer
        
class Player(BasePlayer):

    total_holdings = models.FloatField(default = Constants.endowment)
    total_quantity = models.FloatField(default = Constants.initial_quantity)

    high_risk_quantity = models.IntegerField(default = Constants.initial_quantity/2)
    high_risk_holdings = models.FloatField(default = Constants.endowment/2)

    low_risk_quantity = models.IntegerField(default = Constants.initial_quantity/2)
    low_risk_holdings = models.FloatField(default = Constants.endowment/2)

    orders_issued = models.LongStringField(default = "") 

    bonus = models.FloatField(default = 0)

    def set_payoff(self): 
        pass

    def parse_orders(self): 

        orders_issued = list(map(lambda order: ast.literal_eval(order),self.orders_issued.split("-")[:-1]))
        return orders_issued

    def update_issuer_holdings(self,order,price,quantity):

        if order["Action"] == "Buy":

            if order["Asset"] == "High":
                self.high_risk_quantity -= quantity 
                self.high_risk_holdings += quantity * price
            else: 
                self.low_risk_quantity -= quantity 
                self.low_risk_holdings += quantity * price 
        else: 

            if order["Asset"] == "High":
                self.high_risk_quantity += quantity 
                self.high_risk_holdings -= quantity * price
            else: 
                self.low_risk_quantity += quantity 
                self.low_risk_holdings -= quantity * price

        self.total_holdings = self.high_risk_holdings + self.low_risk_holdings
        self.total_quantity = self.high_risk_quantity + self.low_risk_quantity
    
    def live_auction(self, data):

        data["player_id"] = self.id_in_group
    
        if data["Type"] == "Limit":

            data["order_id"] = self.group.limit_orders

            self.group.limit_orders += 1
            
            self.orders_issued += str(data) + "-"

            if data["Asset"] == "High": 
                self.group.high_risk_orders += str(data) + "-"
                self.group.high_risk_limit_orders += str(data) + "-"
            else: 
                self.group.low_risk_orders += str(data) + "-"
                self.group.low_risk_limit_orders += str(data) + "-"
    
        # cualquier operacion que se quiera realizar con las ordenes se hace a partir del mapeo
        high_risk_orders = list(map(lambda order: ast.literal_eval(order),self.group.high_risk_orders.split("-")[:-1]))
        low_risk_orders = list(map(lambda order: ast.literal_eval(order),self.group.low_risk_orders.split("-")[:-1]))

        orders_issued = self.parse_orders() # obtener ordenes en formato de dict - lista

        if data["Type"] == "Market": 

            data["order_id"] = self.group.market_orders

            self.group.market_orders += 1

            if data["Asset"] == "High": 

                self.group.high_risk_market_orders += str(data) + "-"

                high_risk_orders_rest = filter(lambda order: order["player_id"] != self.id_in_group ,high_risk_orders)

                if data["Action"] == "Buy":

                    high_risk_sell_offers = filter(lambda order: order["Action"] == "Sell", high_risk_orders_rest)

                    high_risk_best_sell_offer = sorted(high_risk_sell_offers, key = lambda order: order["Price"])[0]

                    quantity_to_buy = data["Quantity"] if data["Quantity"] <= high_risk_best_sell_offer["Quantity"] else high_risk_best_sell_offer["Quantity"]

                    self.high_risk_quantity += quantity_to_buy 
                    self.high_risk_holdings -= quantity_to_buy * high_risk_best_sell_offer["Price"]

                    order_issuer = self.group.get_order_issuer(high_risk_best_sell_offer)
                    order_issuer.update_issuer_holdings(data,high_risk_best_sell_offer["Price"],quantity_to_buy)
                    #delete offer from high_risk_orders
                    high_risk_orders.remove(high_risk_best_sell_offer)

                else: 

                    high_risk_buy_offers = filter(lambda order: order["Action"] == "Buy", high_risk_orders_rest)

                    high_risk_best_buy_offer = sorted(high_risk_buy_offers, key = lambda order: order["Price"])[-1]

                    quantity_to_sell = data["Quantity"] if data["Quantity"] <= high_risk_best_buy_offer["Quantity"] else high_risk_best_buy_offer["Quantity"]

                    self.high_risk_quantity -= quantity_to_sell 
                    self.high_risk_holdings += quantity_to_sell * high_risk_best_buy_offer["Price"]

                    order_issuer = self.group.get_order_issuer(high_risk_best_buy_offer)
                    order_issuer.update_issuer_holdings(data,high_risk_best_buy_offer["Price"],quantity_to_sell)

                    high_risk_orders.remove(high_risk_best_buy_offer)

            if data["Asset"] == "Low": 

                self.group.low_risk_market_orders += str(data) + "-"

                low_risk_orders_rest = filter(lambda order: order["player_id"] != self.id_in_group ,low_risk_orders)

                if data["Action"] == "Buy":

                    low_risk_sell_offers = filter(lambda order: order["Action"] == "Sell", low_risk_orders_rest)

                    low_risk_best_sell_offer = sorted(low_risk_sell_offers, key = lambda order: order["Price"])[0]

                    quantity_to_buy = data["Quantity"] if data["Quantity"] <= low_risk_best_sell_offer["Quantity"] else low_risk_best_sell_offer["Quantity"]

                    self.low_risk_quantity += quantity_to_buy 
                    self.low_risk_holdings -= quantity_to_buy * low_risk_best_sell_offer["Price"]

                    order_issuer = self.group.get_order_issuer(low_risk_best_sell_offer)
                    order_issuer.update_issuer_holdings(data,low_risk_best_sell_offer["Price"],quantity_to_buy)

                    #delete offer from high_risk_orders
                    low_risk_orders.remove(low_risk_best_sell_offer)

                else: 

                    low_risk_buy_offers = filter(lambda order: order["Action"] == "Buy", low_risk_orders_rest)

                    low_risk_best_buy_offer = sorted(low_risk_buy_offers, key = lambda order: order["Price"])[-1]

                    quantity_to_sell = data["Quantity"] if data["Quantity"] <= low_risk_best_buy_offer["Quantity"] else low_risk_best_buy_offer["Quantity"]

                    self.low_risk_quantity -= quantity_to_sell 
                    self.low_risk_holdings += quantity_to_sell * low_risk_best_buy_offer["Price"]

                    order_issuer = self.group.get_order_issuer(low_risk_best_buy_offer)
                    order_issuer.update_issuer_holdings(data,low_risk_best_buy_offer["Price"],quantity_to_sell)

                    low_risk_orders.remove(low_risk_best_buy_offer)

            self.total_holdings = self.low_risk_holdings + self.high_risk_holdings 
            self.total_quantity = self.low_risk_quantity + self.high_risk_quantity

        response = {
            0 : {
                "high_risk_orders" : high_risk_orders,
                "low_risk_orders" : low_risk_orders,
                "players" : self.group.get_players_parser(),
            },
        }

        # updating the orders "database"
        if high_risk_orders: 
            self.group.high_risk_orders = "-".join(list(map(lambda order: str(order),high_risk_orders))) + "-"
        if low_risk_orders: 
            self.group.low_risk_orders = "-".join(list(map(lambda order: str(order),low_risk_orders))) + "-"

        # print(response)

        return response
