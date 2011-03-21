# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""

from vigilo.common.conf import settings
settings.load_file('settings_tests.ini')

from vigilo.models.configure import configure_db
configure_db(settings['database'], 'sqlalchemy_')
