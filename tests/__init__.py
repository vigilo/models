# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""

import sys
from vigilo.common.conf import settings
settings.load_file('settings_tests.ini')

from vigilo.models.configure import configure_db

configure_db(settings['database'], 'sqlalchemy_')

# Ce hack est nécessaire afin de pouvoir utiliser pkg_resources
# sur le dossier "testdata" et obtenir les scripts de migration
# de test.
import tests
sys.path[0:0] = tests.__path__
