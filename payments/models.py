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
    
    edad = models.IntegerField(
        label = 'Indica tu edad:',
        choices = [i for i in range(18,40)]
    )

    #variable de interes 
    sexo = models.IntegerField(
        label = 'Indica tu sexo:',
        widget = widgets.RadioSelectHorizontal,
        choices = [[0,'Hombre'],[1,'Mujer']],
    )

    distrito_residencia = models.IntegerField(
        label = 'Indica tu distrito de residencia',
        choices = [
            [0,"Ancón"],
            [1,"Ate"],
            [2,"Barranco"],
            [3,"Breña"],
            [4,"Carabayllo"],
            [5,"Chaclacayo"],
            [6,"Chorrillos"],
            [7,"Cieneguilla"],
            [8,"Comas"],
            [9,"El Agustino"],
            [10,"Independencia"],
            [11,"Jesús María"],
            [12,"La Molina"],
            [13,"La Victoria"],
            [14,"Lima"],
            [15,"Lince"],
            [16,"Los Olivos"],
            [17,"Lurigancho"],
            [18,"Lurín"],
            [19,"Magdalena del Mar"],
            [20,"Miraflores"],
            [21,"Pachacámac"],
            [22,"Pucusana"],
            [23,"Pueblo Libre"],
            [24,"Puente Piedra"],
            [25,"Punta Hermosa"],
            [26,"Punta Negra"],
            [27,"Rimac"],
            [28,"San Bartolo"],
            [29,"San Borja"],
            [30,"San Isidro"],
            [31,"San Juan de Lurigancho"],
            [32,"San Juan de Miraflores"],
            [33,"San Luis"],
            [34,"San Martín de Porres"],
            [35,"San Miguel"],
            [36,"Santa Anita"],
            [37,"Santa Maria del Mar"],
            [38,"Santa Rosa"],
            [39,"Santiago de Surco"],
            [40,"Surquillo"],
            [41,"Villa El Salvador"],
            [42,"Villa María del Triunfo"],
            [43,"Bellavista"],
            [44,"Carmen de la Legua Reynoso"],
            [45,"La Perla"],
            [46,"La Punta"],
            [47,"Ventanilla"],
            [48,"Mi Perú"],
        ], 
    )

    escala = models.IntegerField(
        label = 'Indica en qué escala de pagos te encuentras:',
        choices = [1,2,3,4,5,6]
    )

    ciclo = models.IntegerField(
        label = 'Indica en qué ciclo te encuentras',
        choices = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    )

    carrera = models.IntegerField(
        label = '¿Qué carrera estás cursando?',
        choices = [
            [0,"Negocios Internacionales"],
            [1,"Economía"],
            [2,"Finanzas"],
            [3,"Marketing"],
            [4,"Ingenieria Empresarial"],
            [5, "Ingenieria de la Información"],
            [6, "Administración de Empresas"],
            [7,"Derecho Empresarial"],
            [8,"Contabilidad"]]
    )

    nivel_estudios_padres = models.IntegerField(
        label = 'Indica el nivel de estudio de tus padres',
        choices = [
            [0,"Ninguno"],
            [1,"Primaria"],
            [2,"Secundaria"],
            [3,"Superior no universitaria"],
            [4,"Superior universitaria"],
            [5,"Post-grado universitario"]]
    )

    participado_antes = models.IntegerField(
        label = '¿Has participado antes en un experimento del E2LabUP?',
        widget = widgets.RadioSelectHorizontal,
        choices =[[1,'Si'], [0,'No']]
    )