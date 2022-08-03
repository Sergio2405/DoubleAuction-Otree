from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Instructions(Page):
    
    def is_displayed(self):
        return self.player.round_number == 1

class Auction(Page):

    timeout_seconds = 30
    timer_text = 'El mercado cierra en :'

    live_method = 'live_auction'

    def vars_for_template(self): 
        return dict(
            player_id = self.player.id_in_group
        )

class Statistics(Page):

    timeout_seconds = 40
    timer_text = 'Tiempo restante para ver sus resultados :'

    def vars_for_template(self):
        pass

    def before_next_page(self):
        self.group.generate_ranking() 
        for player in self.group.get_players():
            player.set_payoff()

class Ranking(Page): 

    def vars_for_template(self): 
        
        players_ranking = sorted(self.group.get_players(), key = lambda player: player.payoff, reverse = True)
        dict(
            players_ranking = players_ranking,
            player_id = self.player.id
        )

page_sequence = [Instructions, Auction, Statistics, Ranking]
