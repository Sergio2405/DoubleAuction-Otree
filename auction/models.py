from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,

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
    num_rounds = 6 + 2 # 2 rondas de practica

    time_per_round = 2 # time in minutes

    endowment = 2000 # points
    initial_quantity = 40 # total initial asset units
    buyback_prices = {
        "High" : [[15,65],[0.8,0.2]],
        "Low" : [[20,30],[0.5,0.5]]
    }

    pay_round = random.randint(3,num_rounds) # chossing pay round
    
    treatments = dict(
        PR = {},
        PR1 = {},
        AB = {"fixed": 3.75, "bonus": 0.0004, "exceed": 1000},
        TB1 = {"fixed" : 3.75, "bonus": 3.75, "threshold": 0.30},
        TB2 = {"fixed" : 3.75, "bonus": 3.75, "threshold": 0.70},
        AP = {"fixed": 7.5, "penalty": 0.0015, "below": 5000},
        TP1 = {"fixed" : 7.5, "penalty": 3.75, "threshold": 0.30},
        TP2 = {"fixed" : 7.5, "penalty": 3.75, "threshold": 0.70},
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

    treatment = models.StringField(default = "")

    # buyback prices 
    high_risk_buyback = models.IntegerField(default = 0)
    low_risk_buyback = models.IntegerField(default = 0)

    # cantidad de ordenes segun tipo
    limit_orders = models.IntegerField(default = 0) # num de limit orders
    market_orders = models.IntegerField(default = 0) # num de market orders

    # variables para obtener precio de mercado (precio por ronda)
    high_risk_orders_count = models.IntegerField(default = 0)
    low_risk_orders_count = models.IntegerField(default = 0)
    
    high_risk_acum_price = models.FloatField(default = 0)
    low_risk_acum_price = models.FloatField(default = 0)

    # volumen por mercado
    high_risk_volume = models.FloatField(default = 0)
    low_risk_volume = models.FloatField(default = 0)

    demand_high_risk_price = models.FloatField(default = 0)
    demand_high_risk_quantity = models.FloatField(default = 0)
    demand_high_risk_offers = models.IntegerField(default = 0)

    supply_high_risk_price = models.FloatField(default = 0)
    supply_high_risk_quantity = models.FloatField(default = 0)
    supply_high_risk_offers = models.IntegerField(default = 0)

    demand_low_risk_price = models.FloatField(default = 0)
    demand_low_risk_quantity = models.FloatField(default = 0)
    demand_low_risk_offers = models.IntegerField(default = 0)

    supply_low_risk_price = models.FloatField(default = 0)
    supply_low_risk_quantity = models.FloatField(default = 0)
    supply_low_risk_offers = models.IntegerField(default = 0)

    #### vars usadas como almacenadores de ordenes temporales (vars auxiliares) #####
    high_risk_orders = models.LongStringField(default = "")
    low_risk_orders = models.LongStringField(default = "")
    
    def clear_orders(self):
        self.high_risk_orders = ""
        self.low_risk_orders = ""

    def generate_ranking(self): 

        players = self.get_players()
        for player in players: 
            
            high_risk_quantity = 0 if player.high_risk_quantity < 0 else player.high_risk_quantity
            low_risk_quantity = 0 if player.low_risk_quantity < 0 else player.low_risk_quantity

            player.earnings = high_risk_quantity * self.high_risk_buyback + low_risk_quantity * self.low_risk_buyback + player.total_holdings

        players = self.get_players()
        players_ranking = sorted(players, key = lambda player: player.earnings, reverse = True)

        return players_ranking
    
    def set_payoffs(self):

        players = self.get_players()
        players_ranking = self.generate_ranking()
        treatments = Constants.treatments

        for player in players: 

            if self.treatment == "AB":

                treatment = treatments["AB"]

                if player.earnings > treatment["exceed"]:
                    bonus_payment = treatment["bonus"] * (player.earnings - treatment["exceed"])
                    player.bonus_penalty = round(bonus_payment,2)
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
                    penalty_payment = treatment["penalty"] * abs(player.earnings - treatment["below"]) 
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

            elif self.treatment == "TP2":  
                
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

            else:

                player.payoff = 0
                player.bonus_penalty = 0
                player.fixed_payment = 0

            if player.round_number == Constants.pay_round:
                player.participant.vars["payoff_auction"] = player.payoff

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

    def get_order_issuer(self, order): 

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

    demand_high_risk_price = models.FloatField(default = 0)
    demand_high_risk_quantity = models.FloatField(default = 0)
    demand_high_risk_offers = models.IntegerField(default = 0)

    supply_high_risk_price = models.FloatField(default = 0)
    supply_high_risk_quantity = models.FloatField(default = 0)
    supply_high_risk_offers = models.IntegerField(default = 0)

    demand_low_risk_price = models.FloatField(default = 0)
    demand_low_risk_quantity = models.FloatField(default = 0)
    demand_low_risk_offers = models.IntegerField(default = 0)

    supply_low_risk_price = models.FloatField(default = 0)
    supply_low_risk_quantity = models.FloatField(default = 0)
    supply_low_risk_offers = models.IntegerField(default = 0)

    market_orders = models.IntegerField(default = 0)
    limit_orders = models.IntegerField(default = 0)

    bonus_penalty = models.FloatField(default = 0)
    fixed_payment = models.FloatField(default = 0)

    earnings = models.FloatField(default = 0)

    def update_issuer_holdings(self, order, price, quantity):

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

            if data["Asset"] == "High": 

                self.group.high_risk_orders += str(data) + "-"

                if data["Action"] == "Buy":

                    self.demand_high_risk_price += data["Price"]
                    self.demand_high_risk_quantity += data["Quantity"]
                    self.demand_high_risk_offers += 1

                    self.group.demand_high_risk_price += data["Price"]
                    self.group.demand_high_risk_quantity += data["Quantity"]
                    self.group.demand_high_risk_offers += 1

                    self.limit_orders += 1
                    self.group.limit_orders += 1

                else:

                    self.supply_high_risk_price += data["Price"]
                    self.supply_high_risk_quantity += data["Quantity"]
                    self.supply_high_risk_offers += 1

                    self.group.supply_high_risk_price += data["Price"]
                    self.group.supply_high_risk_quantity += data["Quantity"]
                    self.group.supply_high_risk_offers += 1

                    self.limit_orders += 1
                    self.group.limit_orders += 1

            else: 

                self.group.low_risk_orders += str(data) + "-"

                if data["Action"] == "Buy":

                    self.demand_low_risk_price += data["Price"]
                    self.demand_low_risk_quantity += data["Quantity"]
                    self.demand_low_risk_offers += 1

                    self.group.demand_low_risk_price += data["Price"]
                    self.group.demand_low_risk_quantity += data["Quantity"]
                    self.group.demand_low_risk_offers += 1

                    self.limit_orders += 1
                    self.group.limit_orders += 1

                else:

                    self.group.supply_low_risk_price += data["Price"]
                    self.group.supply_low_risk_quantity += data["Quantity"]
                    self.group.supply_low_risk_offers += 1

                    self.limit_orders += 1
                    self.group.limit_orders += 1
    
        # cualquier operacion que se quiera realizar con las ordenes se hace a partir del mapeo
        high_risk_orders = list(map(lambda order: ast.literal_eval(order),self.group.high_risk_orders.split("-")[:-1]))
        low_risk_orders = list(map(lambda order: ast.literal_eval(order),self.group.low_risk_orders.split("-")[:-1]))

        if data["Type"] == "Market": 

            data["order_id"] = self.group.market_orders

            if high_risk_orders:
                
                if data["Asset"] == "High": 

                    high_risk_orders_rest = list(filter(lambda order: order["player_id"] != self.id_in_group ,high_risk_orders))

                    if data["Action"] == "Buy" and high_risk_orders_rest:

                        high_risk_sell_offers = filter(lambda order: order["Action"] == "Sell", high_risk_orders_rest)

                        high_risk_best_sell_offer = sorted(high_risk_sell_offers, key = lambda order: order["Price"])[0]

                        quantity_to_buy = data["Quantity"] if data["Quantity"] <= high_risk_best_sell_offer["Quantity"] else high_risk_best_sell_offer["Quantity"]

                        self.high_risk_quantity += quantity_to_buy 
                        self.high_risk_holdings -= quantity_to_buy * high_risk_best_sell_offer["Price"]

                        self.demand_high_risk_price += high_risk_best_sell_offer["Price"]
                        self.demand_high_risk_quantity += quantity_to_buy
                        self.demand_high_risk_offers += 1

                        self.group.demand_high_risk_price += high_risk_best_sell_offer["Price"]
                        self.group.demand_high_risk_quantity += quantity_to_buy
                        self.group.demand_high_risk_offers += 1

                        self.group.high_risk_volume += quantity_to_buy 

                        self.group.high_risk_orders_count += 1
                        self.group.high_risk_acum_price += high_risk_best_sell_offer["Price"]

                        self.market_orders += 1
                        self.group.market_orders += 1

                        order_issuer = self.group.get_order_issuer(high_risk_best_sell_offer)
                        order_issuer.update_issuer_holdings(data,high_risk_best_sell_offer["Price"],quantity_to_buy)
                        #delete offer from high_risk_orders
                        high_risk_orders.remove(high_risk_best_sell_offer)

                    else: 

                        if high_risk_orders_rest:

                            high_risk_buy_offers = filter(lambda order: order["Action"] == "Buy", high_risk_orders_rest)

                            high_risk_best_buy_offer = sorted(high_risk_buy_offers, key = lambda order: order["Price"])[-1]

                            quantity_to_sell = data["Quantity"] if data["Quantity"] <= high_risk_best_buy_offer["Quantity"] else high_risk_best_buy_offer["Quantity"]

                            self.high_risk_quantity -= quantity_to_sell 
                            self.high_risk_holdings += quantity_to_sell * high_risk_best_buy_offer["Price"]

                            self.supply_high_risk_price += high_risk_best_buy_offer["Price"]
                            self.supply_high_risk_quantity += quantity_to_sell
                            self.supply_high_risk_offers += 1

                            self.group.supply_high_risk_price += high_risk_best_buy_offer["Price"]
                            self.group.supply_high_risk_quantity += quantity_to_sell
                            self.group.supply_high_risk_offers += 1

                            self.group.high_risk_volume += quantity_to_sell

                            self.group.high_risk_orders_count += 1
                            self.group.high_risk_acum_price += high_risk_best_buy_offer["Price"]

                            self.market_orders += 1
                            self.group.market_orders += 1

                            order_issuer = self.group.get_order_issuer(high_risk_best_buy_offer)
                            order_issuer.update_issuer_holdings(data,high_risk_best_buy_offer["Price"],quantity_to_sell)

                            high_risk_orders.remove(high_risk_best_buy_offer)

            if low_risk_orders:

                if data["Asset"] == "Low": 

                    low_risk_orders_rest = list(filter(lambda order: order["player_id"] != self.id_in_group ,low_risk_orders))

                    if data["Action"] == "Buy" and low_risk_orders_rest:

                        low_risk_sell_offers = filter(lambda order: order["Action"] == "Sell", low_risk_orders_rest)

                        low_risk_best_sell_offer = sorted(low_risk_sell_offers, key = lambda order: order["Price"])[0]

                        quantity_to_buy = data["Quantity"] if data["Quantity"] <= low_risk_best_sell_offer["Quantity"] else low_risk_best_sell_offer["Quantity"]

                        self.low_risk_quantity += quantity_to_buy 
                        self.low_risk_holdings -= quantity_to_buy * low_risk_best_sell_offer["Price"]

                        self.demand_low_risk_price += low_risk_best_sell_offer["Price"]
                        self.demand_low_risk_quantity += quantity_to_buy
                        self.demand_low_risk_offers += 1

                        self.group.demand_low_risk_price += low_risk_best_sell_offer["Price"]
                        self.group.demand_low_risk_quantity += quantity_to_buy
                        self.group.demand_low_risk_offers += 1

                        self.group.low_risk_volume += quantity_to_buy

                        self.group.low_risk_orders_count += 1
                        self.group.low_risk_acum_price += low_risk_best_sell_offer["Price"]

                        self.market_orders += 1
                        self.group.market_orders += 1

                        order_issuer = self.group.get_order_issuer(low_risk_best_sell_offer)
                        order_issuer.update_issuer_holdings(data,low_risk_best_sell_offer["Price"],quantity_to_buy)

                        #delete offer from high_risk_orders
                        low_risk_orders.remove(low_risk_best_sell_offer)

                    else: 

                        if low_risk_orders_rest:

                            low_risk_buy_offers = filter(lambda order: order["Action"] == "Buy", low_risk_orders_rest)

                            low_risk_best_buy_offer = sorted(low_risk_buy_offers, key = lambda order: order["Price"])[-1]

                            quantity_to_sell = data["Quantity"] if data["Quantity"] <= low_risk_best_buy_offer["Quantity"] else low_risk_best_buy_offer["Quantity"]

                            self.low_risk_quantity -= quantity_to_sell 
                            self.low_risk_holdings += quantity_to_sell * low_risk_best_buy_offer["Price"]

                            self.supply_low_risk_price += low_risk_best_buy_offer["Price"]
                            self.supply_low_risk_quantity += quantity_to_sell
                            self.supply_low_risk_offers += 1

                            self.group.supply_low_risk_price += low_risk_best_buy_offer["Price"]
                            self.group.supply_low_risk_quantity += quantity_to_sell
                            self.group.supply_low_risk_offers += 1

                            self.group.low_risk_volume += quantity_to_sell

                            self.group.low_risk_orders_count += 1
                            self.group.low_risk_acum_price += low_risk_best_buy_offer["Price"]

                            self.market_orders += 1
                            self.group.market_orders += 1

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
