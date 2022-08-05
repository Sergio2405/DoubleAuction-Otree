from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Instructions(Page):
    
    def is_displayed(self):
        return self.player.round_number == 1

class AuctionWaitPage(WaitPage):
    pass

class Auction(Page):

    # timeout_seconds = 30
    # timer_text = 'El mercado cierra en :'

    live_method = 'live_auction'

    def vars_for_template(self): 
        return dict(
            player_id = self.player.id_in_group
        )

class Statistics(Page):

    # timeout_seconds = 30
    # timer_text = 'Tiempo restante para ver sus resultados :'

    def vars_for_template(self):

        high_risk_quantity = self.player.high_risk_quantity
        low_risk_quantity = self.player.low_risk_quantity
        high_risk_buyback = self.group.high_risk_buyback
        low_risk_buyback = self.group.low_risk_buyback

        high_buyback_holdings = high_risk_quantity * high_risk_buyback
        low_buyback_holdings = low_risk_quantity * low_risk_buyback

        return dict(
            high_risk_quantity = high_risk_quantity,
            low_risk_quantity = low_risk_quantity,
            high_risk_buyback = high_risk_buyback,
            low_risk_buyback = low_risk_buyback,
            high_buyback_holdings = high_buyback_holdings,
            low_buyback_holdings = low_buyback_holdings,
            total_holdings = high_buyback_holdings + low_buyback_holdings
        )

class RankingWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Ranking(Page): 

    def vars_for_template(self): 

        players = self.group.get_players()
        players_ranking = sorted(players, key = lambda player: player.earnings, reverse = True)
      
        return dict(
            players_ranking = players_ranking,
            player_id = self.player.id_in_group
        )

page_sequence = [Instructions, AuctionWaitPage, Auction, Statistics, RankingWaitPage, Ranking]
