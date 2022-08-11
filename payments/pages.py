from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Pagos(Page):
    
    def vars_for_template(self):

        apps = self.session.config['app_names']

        pagos_apps = {}
        pago_total = 0
        pago_total_soles = 0

        for app in self.session.config['app_sequence'][1:-1]:

            name = apps[app]
            pago = self.player.participant.vars['payoff_'+app]
            
            pagos_apps[name] = pago

            exchange_rate =  self.session.config["exchange_rates"]["Points"] if name != "Cuarta" else self.session.config["exchange_rates"]["Solex"]

            pago_soles = pago *  exchange_rate

            pago_total += pago
            
            pago_total_soles += pago_soles

        return dict(
            pagos_apps = pagos_apps,
            pago_total = pago_total,
            participant_fee = self.session.config["participant_fee"],
            pago_total_soles = pago_total_soles,
            pago_total_soles_fee = pago_total_soles + self.session.config["participant_fee"],
            exchange_points = self.session.config['exchange_rates']['Points'],
            exchange_solex = self.session.config['exchange_rates']['Solex']
        )


class Pagos_info(Page):
    def vars_for_template(self):
        return dict(participant_id=self.participant.label)

page_sequence = [Pagos,Pagos_info]

