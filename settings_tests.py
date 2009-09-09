
VIGILO_MODELS_BDD_BASENAME = ''

VIGILO_ALL_DEFAULT_LANGUAGE = 'fr'

# Configuration for Vigilo database
# Can't split off the pylons / tg2 sa_engine configuration
# from the config of a complete wsgiapp, which uses paste.deploy
# and has no modularity (can't include another config, etc).
# So this is a slight bit of duplication.
# Also, maybe switch to yaml, or repoze.configuration, and use sa.engine_from_config
VIGILO_SQLALCHEMY = {
    'url': 'sqlite:///:memory:',
}

