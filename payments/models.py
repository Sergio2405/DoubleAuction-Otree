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
    
    #preguntas de sugerencia

    interfaz = models.IntegerField(
        label = '¿Que tal te pareció la interfaz (la parte visual) del experimento? 20 si fue muy buena y 0 lo contrario',
        choices = [i for i in range(0,21)]
    )

    instrucciones = models.IntegerField(
        label = '¿Que tan entendibles eran las instrucciones? 20 si es que si lo eran y 0 lo contrario',
        choices = [i for i in range(0,21)]
    )

    espera = models.IntegerField(
        label = '¿Que tal te pareció la fluidez del experimento?, 20 si no hubo trabas o demoras inncesarias y 0 lo contrario',
        choices = [i for i in range(0,21)]
    )

    preguntas_control = models.IntegerField(
        label = '¿Consideras que las preguntas de control previo al inicio de cada parte del experimento te ayudaron a entender mejor cada tarea involucrada? 20 si sentiste que sí y 0 si sentiste que era una pérdida de tiempo',
        choices = [i for i in range(0,21)]
    )

    sugerencia = models.LongStringField(
         label = 'Por favor dejanos una sugerencia general, tanto puntos positivos como negativos'  
    )

    #preguntas de estereotipo

    pregunta1 = models.FloatField(default = 0)
    pregunta2 = models.FloatField(default = 0)
