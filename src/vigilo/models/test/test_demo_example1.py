# -*- coding: utf-8 -*-

import unittest
import transaction
from controller import setup_db, teardown_db
from vigilo.models.demo.example1 import main
from vigilo.models.tables import StateName
from vigilo.models.session import DBSession
from vigilo.models.websetup import populate_db

class TestDemoExample1(unittest.TestCase):
    def setUp(self):
        super(TestDemoExample1, self).setUp()
        populate_db(DBSession.bind, False)
#        setup_db()
#        DBSession.add(StateName(statename=u'OK', order=1))
#        DBSession.add(StateName(statename=u'UNKNOWN', order=2))
#        DBSession.add(StateName(statename=u'WARNING', order=3))
#        DBSession.add(StateName(statename=u'CRITICAL', order=4))
#        DBSession.add(StateName(statename=u'UP', order=1))
#        DBSession.add(StateName(statename=u'UNREACHABLE', order=2))
#        DBSession.add(StateName(statename=u'DOWN', order=4))
#        DBSession.flush()

    def tearDown(self):
        DBSession.expunge_all()
        teardown_db()
        super(TestDemoExample1, self).tearDown()

    def test_demo(self):
        """Démonstration example1"""
        main()
        DBSession.flush()
