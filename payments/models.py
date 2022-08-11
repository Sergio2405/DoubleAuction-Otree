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

doc = """

Payment app: Final Payments, Comments & Payment Info

"""

class Constants(BaseConstants):
    name_in_url = 'payments'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    
    def vars_for_admin_report(self):

        apps = self.session.config['app_sequence'][1:-1]

        players = self.get_players()
        payments = {}
        for player in players:
            player_payments = {}
            total = 0
            # player_payments['id'] = player.id_in_group
            for app in apps:
                exchange_rate =  self.session.config["exchange_rates"]["Points"] if app != "measure_task" else self.session.config["exchange_rates"]["Solex"]
                player_payments[app] = player.participant.vars['payoff_'+app] * exchange_rate
                total += player_payments[app]
            player_payments['Total'] = total + 5

            payments[player.id_in_group] = player_payments 
            
        return dict(
                payments = payments
            )

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass