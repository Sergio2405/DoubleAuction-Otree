from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Auction(Page):

    live_method = 'live_auction'

    def vars_for_template(self): 
        return dict(
            player_id = self.player.id_in_group
        )

page_sequence = [Auction]
