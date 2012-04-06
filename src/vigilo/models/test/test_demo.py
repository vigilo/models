# -*- coding: utf-8 -*-
# Copyright (C) 2011-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Teste les scénarios de démonstration.
"""

import unittest
from vigilo.models.test.controller import teardown_db
from vigilo.models import demo
from vigilo.models.session import DBSession
from vigilo.models.websetup import populate_db

class TestDemo(unittest.TestCase):
    """
    Vérifie que les scénarios de démonstration
    s'exécutent correctement.
    """
    def setUp(self):
        super(TestDemo, self).setUp()
        populate_db(DBSession.bind, False)

    def tearDown(self):
        DBSession.expunge_all()
        teardown_db()
        super(TestDemo, self).tearDown()

    def test_demo(self):
        """Démonstration 'example1'."""
        demo.example1.main()
        DBSession.flush()
