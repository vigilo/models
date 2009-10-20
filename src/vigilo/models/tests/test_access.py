# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Test suite for Access class"""
from vigilo.models import Access
from vigilo.models.tests import ModelTest, setup_db, teardown_db
from vigilo.models.session import DBSession
from datetime import datetime
import unittest
import transaction

class TestAccess(ModelTest):
    """Tests unitaires de la table Access"""

    klass = Access
    attrs = {
        'message': u'This is a test',
        'timestamp': datetime.now(),
    }

    def __init__(self):
        ModelTest.__init__(self)


class TestAccessFunc(unittest.TestCase):
    """Tests fonctionnels de la classe Access"""

    def setUp(self):
        transaction.begin()

    def tearDown(self):
        DBSession.rollback()

    def test_add_login(self):
        """Vérifie que l'enregistrement des connexions fonctionne."""

        Access.add_login(u'foo', u'app1')
        count = DBSession.query(Access).filter(
            Access.message == u"User 'foo' logged in (app1).").count()
        self.assertEquals(1, count,
            "Expected exactly 1 user login message, got %d." % count)
        
    def test_add_logout(self):
        """Vérifie que l'enregistrement des déconnexions fonctionne."""

        Access.add_logout(u'bar', u'app2')
        count = DBSession.query(Access).filter(
            Access.message == u"User 'bar' logged out (app2).").count()
        self.assertEquals(1, count,
            "Expected exactly 1 user logout message, got %d." % count)

