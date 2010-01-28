# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Test suite for ApplicationLog class"""
from datetime import datetime
import unittest

from vigilo.models import ApplicationLog
from vigilo.models.session import DBSession
from vigilo.models.vigilo_bdd_config import metadata

from controller import ModelTest, setup_db, teardown_db

class TestApplicationLog(ModelTest):
    """Tests unitaires de la table ApplicationLog"""

    klass = ApplicationLog
    attrs = {
        'message': u'This is a test',
        'timestamp': datetime.now(),
        'ip': u'127.0.0.1',
        'username': u'foobar',
        'application': u'app',
    }

    def __init__(self):
        ModelTest.__init__(self)


class TestApplicationLogFunc(unittest.TestCase):
    """Tests fonctionnels de la classe ApplicationLog"""

    def tearDown(self):
        """Suppression des données d'initialisation du test."""
        DBSession.rollback()
        DBSession.expunge_all()

    def test_add_login(self):
        """Vérifie que l'enregistrement des connexions fonctionne."""

        ApplicationLog.add_login(u'foo', u'127.0.0.1', u'app1')
        log = DBSession.query(ApplicationLog).one()
        self.assertEquals(u"User logged in.", log.message)
        self.assertEquals(u'app1', log.application)
        self.assertEquals(u'foo', log.username)
        self.assertEquals(u'127.0.0.1', log.ip)

    def test_add_logout(self):
        """Vérifie que l'enregistrement des déconnexions fonctionne."""

        ApplicationLog.add_logout(u'bar', u'127.0.0.2', u'app2')
        log = DBSession.query(ApplicationLog).one()
        self.assertEquals(u"User logged out.", log.message)
        self.assertEquals(u'app2', log.application)
        self.assertEquals(u'bar', log.username)
        self.assertEquals(u'127.0.0.2', log.ip)

