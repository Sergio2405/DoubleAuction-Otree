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

    quantity = models.IntegerField(default = 0)
    holdings = models.IntegerField(default = 0)
    
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
            
        # esto no cambiar
        response = {0:{
            "high_risk_orders" : high_risk_orders,
            "low_risk_orders" : low_risk_orders
        }}

        print(response)

        return response
