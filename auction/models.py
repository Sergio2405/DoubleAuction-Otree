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
import random
import numpy as np

author = 'Sergio Gonzalo Mejia Ramos'

doc = """

Double Auction Market with 2 Assets to trade

"""

class Constants(BaseConstants):

    name_in_url = 'auction'
    players_per_group = None
    num_rounds = 6

    time_per_round = 2 # time in minutes

    endowment = 2000 # points
    initial_quantity = 40 # total initial asset units
    buyback_prices = {
        "High" : [[15,65],[0.8,0.2]],
        "Low" : [[20,30],[0.5,0.5]]
    }
    
    treatments = dict(
        AB = {"fixed": 20, "bonus": 0.01, "exceed": 1000},
        TB1 = {"fixed" : 20, "bonus": 80, "threshold": 0.30},
        TB2 = {"fixed" : 20, "bonus": 80, "threshold": 0.70},
        AP = {"fixed": 100, "penalty": 0.01, "exceed": 1000, "below": 5000},
        TP1 = {"fixed" : 100, "penalty": 80, "threshold": 0.30},
        TP2 = {"fixed" : 100, "penalty": 80, "threshold": 0.70},
    )

class Subsession(BaseSubsession):
    
    def creating_session(self):
      
        group = self.get_groups()[0]
        treatments = list(Constants.treatments.keys())
        group.treatment = treatments[self.round_number-1]

        high_buyback_prices = Constants.buyback_prices["High"].copy()
        low_buyback_prices = Constants.buyback_prices["Low"].copy()
        
        group.high_risk_buyback = np.random.choice(np.array(high_buyback_prices[0]), p = high_buyback_prices[1])
        group.low_risk_buyback = np.random.choice(np.array(low_buyback_prices[0]), p = low_buyback_prices[1])

class Group(BaseGroup):

    # buyback prices 
    high_risk_buyback = models.IntegerField(default = 0)
    low_risk_buyback = models.IntegerField(default = 0)

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

    high_risk_orders_count = models.IntegerField(default = 0)
    low_risk_orders_count = models.IntegerField(default = 0)
    
    high_risk_acum_price = models.FloatField(default = 0)
    low_risk_acum_price = models.FloatField(default = 0)

    low_risk_limit_orders = models.LongStringField(default = "")
    low_risk_market_orders = models.LongStringField(default = "")

    def generate_ranking(self): 

        players = self.get_players()
        for player in players: 
            
            high_risk_quantity = 0 if player.high_risk_quantity < 0 else player.high_risk_quantity
            low_risk_quantity = 0 if player.low_risk_quantity < 0 else player.low_risk_quantity

            player.earnings = high_risk_quantity * self.high_risk_buyback + low_risk_quantity * self.low_risk_buyback

        players = self.get_players()
        players_ranking = sorted(players, key = lambda player: player.earnings, reverse = True)

        print("Ranking generated!")

        return players_ranking
    
    def set_payoffs(self):

        players = self.get_players()
        players_ranking = self.generate_ranking()
        treatments = Constants.treatments

        print("Ranking: ",players_ranking)

        for player in players: 

            if self.treatment == "AB":

                treatment = treatments["AB"]

                if player.earnings > treatment["exceed"]:
                    bonus_payment = treatment["bonus"] * (player.earnings - treatment["exceed"])
                    player.bonus_penalty = bonus_payment
                else: 
                    bonus_payment = 0
                    player.bonus_penalty = round(bonus_payment,2)

                player.fixed_payment = treatment["fixed"]
                
                player.payoff = treatment["fixed"] + bonus_payment

            elif self.treatment == "TB1": # 0.30

                treatment = treatments["TB1"]
                
                bonus_index = round(len(players_ranking) * (1-treatment["threshold"]))
                bonus_players = players_ranking[0:bonus_index]
                
                if player in bonus_players: 
                    player.payoff = treatment["fixed"] + treatment["bonus"]
                    player.bonus_penalty = treatment["bonus"]
                else:
                    player.payoff = treatment["fixed"]
                    player.bonus_penalty = 0

                player.fixed_payment = treatment["fixed"]

            elif self.treatment == "TB2": # 0.70

                treatment = treatments["TB2"]
                
                bonus_index = round(len(players_ranking) * (1-treatment["threshold"]))
                bonus_players = players_ranking[0:bonus_index]
                
                if player in bonus_players: 
                    player.payoff = treatment["fixed"] + treatment["bonus"]
                    player.bonus_penalty = treatment["bonus"]
                else:
                    player.payoff = treatment["fixed"]
                    player.bonus_penalty = 0

                player.fixed_payment = treatment["fixed"]

            elif self.treatment == "AP":
                
                treatment = treatments["AP"]
                if player.earnings < treatment["below"]:
                    penalty_payment = treatment["penalty"] * (player.earnings - treatment["exceed"]) 
                    player.bonus_penalty = penalty_payment
                else:
                    penalty_payment = 0
                    player.bonus_penalty = round(penalty_payment,2)
                 
                player.payoff = treatment["fixed"] - penalty_payment

                player.fixed_payment = treatment["fixed"]

            elif self.treatment == "TP1":  # 0.30
                
                treatment = treatments["TP1"]

                penalty_index = round(len(players_ranking) * (1-treatment["threshold"]))
                penalty_players = players_ranking[penalty_index:]
                
                if player in penalty_players: 
                    player.payoff = treatment["fixed"] - treatment["penalty"]
                    player.bonus_penalty = treatment["penalty"]
                else:
                    player.payoff = treatment["fixed"]
                    player.bonus_penalty = 0

                player.fixed_payment = treatment["fixed"]

            else: 
                
                treatment = treatments["TP2"] # 0.70

                penalty_index = round(len(players_ranking) * (1-treatment["threshold"]))
                penalty_players = players_ranking[penalty_index:]
                
                if player in penalty_players: 
                    player.payoff = treatment["fixed"] - treatment["penalty"]
                    player.bonus_penalty = treatment["penalty"]
                else:
                    player.payoff = treatment["fixed"]
                    player.bonus_penalty = 0
                
                player.fixed_payment = treatment["fixed"]

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
                        "high_risk" : player.high_risk_quantity,
                        "low_risk" : player.low_risk_quantity
                    },
                "prices" : {
                        "high" : 0 if self.high_risk_orders_count == 0 else self.high_risk_acum_price/self.high_risk_orders_count,
                        "low" :  0 if self.low_risk_orders_count == 0 else self.low_risk_acum_price/self.low_risk_orders_count,
                    }
                }

            players_parsed.append(player_dict)

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
    orders_save = models.LongStringField(default = "")

    bonus_penalty = models.FloatField(default = 0)
    fixed_payment = models.IntegerField(default = 0)

    earnings = models.FloatField(default = 0)

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

            if high_risk_orders:
                
                if data["Asset"] == "High": 

                    self.group.high_risk_market_orders += str(data) + "-"

                    high_risk_orders_rest = filter(lambda order: order["player_id"] != self.id_in_group ,high_risk_orders)

                    if data["Action"] == "Buy":

                        high_risk_sell_offers = filter(lambda order: order["Action"] == "Sell", high_risk_orders_rest)

                        high_risk_best_sell_offer = sorted(high_risk_sell_offers, key = lambda order: order["Price"])[0]

                        quantity_to_buy = data["Quantity"] if data["Quantity"] <= high_risk_best_sell_offer["Quantity"] else high_risk_best_sell_offer["Quantity"]

                        self.high_risk_quantity += quantity_to_buy 
                        self.high_risk_holdings -= quantity_to_buy * high_risk_best_sell_offer["Price"]

                        self.group.high_risk_orders_count += 1
                        self.group.high_risk_acum_price += high_risk_best_sell_offer["Price"]

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

                        self.group.high_risk_orders_count += 1
                        self.group.high_risk_acum_price += high_risk_best_buy_offer["Price"]

                        order_issuer = self.group.get_order_issuer(high_risk_best_buy_offer)
                        order_issuer.update_issuer_holdings(data,high_risk_best_buy_offer["Price"],quantity_to_sell)

                        high_risk_orders.remove(high_risk_best_buy_offer)

            if low_risk_orders:

                if data["Asset"] == "Low": 

                    self.group.low_risk_market_orders += str(data) + "-"

                    low_risk_orders_rest = filter(lambda order: order["player_id"] != self.id_in_group ,low_risk_orders)

                    if data["Action"] == "Buy":

                        low_risk_sell_offers = filter(lambda order: order["Action"] == "Sell", low_risk_orders_rest)

                        low_risk_best_sell_offer = sorted(low_risk_sell_offers, key = lambda order: order["Price"])[0]

                        quantity_to_buy = data["Quantity"] if data["Quantity"] <= low_risk_best_sell_offer["Quantity"] else low_risk_best_sell_offer["Quantity"]

                        self.low_risk_quantity += quantity_to_buy 
                        self.low_risk_holdings -= quantity_to_buy * low_risk_best_sell_offer["Price"]

                        self.group.low_risk_orders_count += 1
                        self.group.low_risk_acum_price += low_risk_best_sell_offer["Price"]

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

                        self.group.low_risk_orders_count += 1
                        self.group.low_risk_acum_price += low_risk_best_buy_offer["Price"]

                        order_issuer = self.group.get_order_issuer(low_risk_best_buy_offer)
                        order_issuer.update_issuer_holdings(data,low_risk_best_buy_offer["Price"],quantity_to_sell)

                        low_risk_orders.remove(low_risk_best_buy_offer)

            self.total_holdings = self.low_risk_holdings + self.high_risk_holdings 
            self.total_quantity = self.low_risk_quantity + self.high_risk_quantity

        if  self.group.high_risk_orders != "": 
            aux = ("-".join(list(map(lambda order: str(order),high_risk_orders))) + "-")[0:]
            if aux == "-":
                self.group.high_risk_orders = ""
            else:
                self.group.high_risk_orders = aux
            # print(self.group.high_risk_orders)
        if self.group.low_risk_orders != "": 
            aux  = ("-".join(list(map(lambda order: str(order),low_risk_orders))) + "-")[0:]
            if aux == "-":
                self.group.low_risk_orders = ""
            else:
                self.group.low_risk_orders = aux

        response = {
            0 : {
                "high_risk_orders" : high_risk_orders,
                "low_risk_orders" : low_risk_orders,
                "players" : self.group.get_players_parser(),
            },
        }

        return response