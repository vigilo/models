# -*- coding: utf-8 -*-
"""
Teste les migrations du modèle.
"""

import unittest
from controller import setup_db, teardown_db
from vigilo.models.session import DBSession
from vigilo.models.tables.grouppath import GroupPath
from vigilo.models.demo.functions import add_supitemgroup
import transaction

class TestMigration(unittest.TestCase):
    def setUp(self):
        setup_db()

    def tearDown(self):
        DBSession.rollback()
        DBSession.expunge_all()
        teardown_db()
        transaction.begin()

    def test_grouppath_representations(self):
        """Teste la représentation d'un chemin pour un groupe."""
        add_supitemgroup(u'TestRoot', None)
        root_path = DBSession.query(GroupPath).first()

        self.assertEquals(u'/TestRoot', unicode(root_path))
        self.assertEquals(u'<GroupPath "/TestRoot">', repr(root_path))
