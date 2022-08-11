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

import random as r
from .config import lotteries


author = 'Marco Gutierrez'

doc = """
Tanaka et al. (2010) Measure Task based on CPT
"""


class Constants(BaseConstants):
    name_in_url = 'measure_task'
    players_per_group = None
    num_rounds = 1
    num_breaks = 3
    instructions_template = "measure_task/Instructions.html"
    choices_series1 = [[1,'1'], [2,'2'], [3,'3'], [4,'4'], [5,'5'], [6,'6'], [7,'7'], [8,'8'], [9,'9'], [10,'10'], [11,'11'], [12,'12'], [13,'13'], [14,'14'], [0 ,'Ninguna']]
    choices_series2 = [[15,'15'], [16,'16'], [17,'17'], [18,'18'], [19,'19'], [20,'20'], [21,'21'], [22,'22'], [23,'23'], [24,'24'], [25,'25'], [26,'26'], [27,'27'], [28,'28'], [0,'Ninguna']]
    choices_series3 = [[29,'29'], [30,'30'], [31,'31'], [32,'32'], [33,'33'], [34,'34'], [35,'35'], [0,'Ninguna']]

    endowment = 30

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    first_choice_1 = models.IntegerField(verbose_name='Escojo la lotería A desde la opción 1 hasta la opción:', choices=Constants.choices_series1)
    first_choice_2 = models.IntegerField(verbose_name='Escojo la lotería A desde la opción 15 hasta la opción:', choices=Constants.choices_series2)
    first_choice_3 = models.IntegerField(verbose_name='Escojo la lotería A desde la opción 29 hasta la opción:', choices=Constants.choices_series3)
    second_choice_1 = models.IntegerField(verbose_name='Escojo la lotería B desde la opción:', choices=Constants.choices_series1)
    second_choice_2 = models.IntegerField(verbose_name='Escojo la lotería B desde la opción:', choices=Constants.choices_series2)
    second_choice_3 = models.IntegerField(verbose_name='Escojo la lotería B desde la opción:', choices=Constants.choices_series3)

    random_draw = models.IntegerField(min=1, max=10)
    random_lottery = models.IntegerField(min=1, max=10)
    selected_lottery = models.CharField()

    def set_payoffs(self):
        self.random_draw = r.randrange(1, 11)
        self.random_lottery = r.randrange(1, 36)
        choices_aux_1 = 0
        choices_aux_2 = 0
        choices_aux_3 = 0

        if self.first_choice_1 != 0:
            choices_aux_1 = int(self.first_choice_1)

        if self.first_choice_2 != 0:
            choices_aux_2 = int(self.first_choice_2)

        if self.first_choice_3 != 0:
            choices_aux_3 = int(self.first_choice_3)

        # Esto ocurre si nunca se escogió la opción ninguna para la lotería A
        # Si la loteria escogia alet es menor o igual a mi primer punto de quiebre o segundo o 3ro, se juega A
        if (self.random_lottery <= choices_aux_1) \
                or (15 <= self.random_lottery <= choices_aux_2)\
                or (29 <= self.random_lottery <= choices_aux_3):

            self.selected_lottery = 'A'
            if self.random_draw <= 3:
                self.payoff = lotteries[0][self.random_lottery - 1]["high_paym_A"]
            elif 3 < self.random_draw <= 10:
                self.payoff = lotteries[0][self.random_lottery - 1]["low_paym_A"]

        # Si la loteria escogia alet es mayor a mi primer punto de quiebre o segundo o 3ro, o si nunca escogí
        # alguna loteria A, se juega B
        else:
            self.selected_lottery = 'B'

            if self.random_draw <= 1:
                self.payoff = lotteries[0][self.random_lottery - 1]["high_paym_B"]
            elif 1 < self.random_draw <= 10:
                self.payoff = lotteries[0][self.random_lottery - 1]["low_paym_B"]

        if self.payoff < 0:
            self.participant.vars["payoff_measure_task"] = Constants.endowment + self.payoff
        else:
            self.participant.vars["payoff_measure_task"] = self.payoff
        
        print("prticipant vars",self.participant.vars["payoff_measure_task"])
