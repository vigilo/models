# -*- coding: utf-8 -*-
# Copyright (C) 2011-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Teste les migrations du modèle.
"""

import unittest

import transaction

from vigilo.models.session import DBSession
from vigilo.models.tables.grouppath import GroupPath
from vigilo.models.demo.functions import add_supitemgroup

from vigilo.models.test.controller import setup_db, teardown_db


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

        self.assertEqual(u'/TestRoot', unicode(root_path))
        self.assertEqual(u'<GroupPath "/TestRoot">', repr(root_path))
