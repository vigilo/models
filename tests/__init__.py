# -*- coding: utf-8 -*-
"""Unit test suite for the models of the application."""

from vigilo.common.conf import settings
settings.load_file('settings_tests.ini')

from vigilo.models.configure import configure_db

configure_db(settings['database'], 'sqlalchemy_',
    settings['database']['db_basename'])

from controller import setup_db, teardown_db

def setup():
    """Fonction appelée par nose au début des tests."""
    setup_db()

def teardown():
    """Fonction appelée par nose à la fin des tests."""
    teardown_db()

