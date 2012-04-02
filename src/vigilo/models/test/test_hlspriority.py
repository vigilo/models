# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Tag class"""

import unittest

from vigilo.models.session import DBSession
from vigilo.models.demo import functions
from vigilo.models.tables import StateName, HLSPriority, HighLevelService

from vigilo.models.test.controller import setup_db, teardown_db


class TestHLSPriority(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        """Préparatifs pour les tests."""
        super(TestHLSPriority, self).setUp(*args, **kwargs)
        setup_db()

        self.hls = functions.add_highlevelservice(u'Connexion')
        DBSession.expunge_all()
        DBSession.query(HLSPriority).delete()
        DBSession.flush()
        self.hls = DBSession.query(HighLevelService).one()
        self.statename = DBSession.query(StateName).filter(
            StateName.statename == u'OK').one()


    def tearDown(self):
        """Nettoyage à l'issue des tests."""
        DBSession.rollback()
        DBSession.expunge_all()
        teardown_db()
        super(TestHLSPriority, self).tearDown()

    def test_add_priority_by_id(self):
        """Ajout priorité pour un HLS par ID."""
        self.hls.priorities[StateName.statename_to_value(u'OK')] = 42
        DBSession.merge(self.hls)
        DBSession.flush()
        entry = DBSession.query(HLSPriority).one()
        self.assertEquals(entry.idhls, self.hls.idservice)
        self.assertEquals(entry.idstatename, StateName.statename_to_value(u'OK'))
        self.assertEquals(entry.priority, 42)

    def test_add_priority_by_name(self):
        """Ajout priorité pour un HLS par nom d'état."""
        self.hls.priorities[u'OK'] = 42
        DBSession.flush()
        entry = DBSession.query(HLSPriority).one()
        self.assertEquals(entry.idhls, self.hls.idservice)
        self.assertEquals(entry.idstatename, StateName.statename_to_value(u'OK'))
        self.assertEquals(entry.priority, 42)

    def test_add_priority_by_instance(self):
        """Ajout priorité pour un HLS par instance."""
        self.hls.priorities[self.statename] = 42
        DBSession.flush()
        entry = DBSession.query(HLSPriority).one()
        self.assertEquals(entry.idhls, self.hls.idservice)
        self.assertEquals(entry.idstatename, StateName.statename_to_value(u'OK'))
        self.assertEquals(entry.priority, 42)

    def test_by_hls_and_statename(self):
        """Récupération priorité avec by_hls_and_statename()."""
        self.hls.priorities[u'OK'] = 42
        self.hls.priorities[u'UNKNOWN'] = 43
        entry = HLSPriority.by_hls_and_statename(self.hls, u'OK')
        self.assertEquals(entry.idhls, self.hls.idservice)
        self.assertEquals(entry.idstatename, StateName.statename_to_value(u'OK'))
        self.assertEquals(entry.priority, 42)
