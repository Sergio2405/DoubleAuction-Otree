from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Auction(Page):
    live_method = 'live_auction'

page_sequence = [Auction]
