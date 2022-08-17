from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Instructions(Page):
    
    def is_displayed(self):
        return self.player.round_number == 1
    
class InterfaceInstructions(Page):

    def is_displayed(self):
        return self.player.round_number == 1

class InstructionsWaitPage(WaitPage):
    
    def is_displayed(self):
        return self.player.round_number == 1

class Instructions_Treatment(Page):
    
    def vars_for_template(self):
        return {
            "round_number" : self.player.round_number,
            "treatment": self.group.treatment,
            "treatments" : Constants.treatments,
            "rondita" : self.player.round_number - 2
        }

class AuctionWaitPage(WaitPage):

    title_text = "Entrando al mercado..."
    body_text = "Espere que los demás traders entren al mercado"

class Auction(Page):

    timeout_seconds = 60*Constants.time_per_round
    timer_text = 'El mercado cierra en :'

    live_method = 'live_auction'

    def vars_for_template(self): 
        return dict(
            player_id = self.player.id_in_group
        )

    def before_next_page(self):
        self.group.clear_orders()

class Statistics(Page):

    timeout_seconds = 30
    timer_text = 'Tiempo restante para ver sus resultados :'

    def vars_for_template(self):

        high_risk_quantity = self.player.high_risk_quantity
        low_risk_quantity = self.player.low_risk_quantity
        high_risk_buyback = self.group.high_risk_buyback
        low_risk_buyback = self.group.low_risk_buyback

        high_buyback_holdings = high_risk_quantity * high_risk_buyback
        low_buyback_holdings = low_risk_quantity * low_risk_buyback

        return {
            "high_risk_quantity" : high_risk_quantity,
            "low_risk_quantity" : low_risk_quantity,
            "high_risk_buyback" : high_risk_buyback,
            "low_risk_buyback" : low_risk_buyback,
            "high_buyback_holdings" : high_buyback_holdings,
            "low_buyback_holdings" : low_buyback_holdings,
            "capital" : self.player.total_holdings,
            "total_holdings" : high_buyback_holdings + low_buyback_holdings,
            "total_holdings_capital" : high_buyback_holdings + low_buyback_holdings + self.player.total_holdings
        }

    def before_next_page(self):
        self.group.generate_ranking()

class RankingWaitPage(WaitPage):

    title_text = "Por favor Espere"
    body_text = "Generando ranking de beneficios..."

    after_all_players_arrive = 'set_payoffs'

    def is_displayed(self):
        return self.player.round_number > 2

class Ranking(Page): 

    timeout_seconds = 30
    timer_text = 'Tiempo restante para ver sus resultados :'

    def is_displayed(self):
        return self.player.round_number > 2

    def vars_for_template(self): 

        players = self.group.get_players()
        players_ranking = sorted(players, key = lambda player: player.earnings, reverse = True)

        treatments_not = ["PR", "PR1", "AB", "AP"]
        ranking = True if self.group.treatment not in treatments_not else False

        players_list = players_ranking if ranking else players
      
        return dict(
            players = players_list,
            player_id = self.player.id_in_group
        )

page_sequence = [
    Instructions, 
    InterfaceInstructions,
    InstructionsWaitPage, 
    Instructions_Treatment, 
    AuctionWaitPage, 
    Auction, 
    Statistics, 
    RankingWaitPage, 
    Ranking
]
