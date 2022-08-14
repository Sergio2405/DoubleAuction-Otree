from os import environ

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=5.00, solex_soles = 0.001, points_soles = 1,  doc=""
)

PARTICIPANT_FIELDS = ['payoff_auction','payoff_measure_task']

SESSION_CONFIGS = [
    dict(
       name = 'Tesis_Sergio_Mejia',
       display_name = "Tesis_Sergio_Mejia",
       num_demo_participants = 10,
       app_sequence = ['initial_page', 'auction', 'measure_task', 'payments'],
       app_names = {'auction':'Primera','measure_task':'Segunda'},
       participant_fee = SESSION_CONFIG_DEFAULTS["participation_fee"],
       exchange_rates = {"Solex": SESSION_CONFIG_DEFAULTS["solex_soles"], "Points": SESSION_CONFIG_DEFAULTS["points_soles"]}
    ),
    dict(
        name = 'Auction',
        display_name = "Auction",
        num_demo_participants = 2,
        app_sequence = ['auction'],
    ),
    dict(
        name = 'Tanaka',
        display_name = "Tanaka",
        num_demo_participants = 1,
        app_sequence = ['measure_task'],
    )
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

ROOMS = [
    dict(
        name='econ101',
        display_name='Econ 101 class',
        participant_label_file='_rooms/econ101.txt',
    ),
    dict(
        name='e2labup',
        display_name='E2LabUP - Room para sesiones online',
        participant_label_file='_rooms/e2labup-room.txt',
    ),
    dict(name='live_demo', display_name='Room for live demo (no participant labels)'),
]

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'es'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = ''
USE_POINTS = False

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '#ivtu5g1d3-n9^apznpld@!b9h_f%fqz#mz@yfgje_@mg9jd%!'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']

DEBUG = True