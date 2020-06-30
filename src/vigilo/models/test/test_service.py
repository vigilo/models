# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for LowLevelService & HighLevelService classes"""

import unittest

from nose.tools import assert_equals

from vigilo.models.tables import Service, StateName, \
                                    LowLevelService, HighLevelService
from vigilo.models.session import DBSession
from vigilo.models.demo import functions

from vigilo.models.test.test_tag import TagTestMixin
from vigilo.models.test.controller import ModelTest, setup_db, teardown_db


class TestLowLevelService(ModelTest, TagTestMixin):
    """Test de la classe LowLevelService."""

    klass = LowLevelService
    attrs = {
        'servicename': u'myservice',
    }

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        # Création de l'hôte physique sur lequel portera la dépendance.
        host = functions.add_host(u'myhost')
        return dict(host=host)

    def test_by_host_service_name(self):
        """Récupération d'un LowLevelService par son nom d'hôte/service."""
        ob = LowLevelService.by_host_service_name(
            u'myhost', self.attrs['servicename'])

    def test_default_state(self):
        """L'état initial d'un service de bas niveau est 'UNKNOWN'."""
        assert_equals(u'UNKNOWN', StateName.value_to_statename(
            DBSession.query(self.klass).one().state.state))

    def test_collector_relation(self):
        """Bon fonctionnement de l'association service -> collector."""
        service = DBSession.query(self.klass).one()
        collector = functions.add_lowlevelservice(
            service.host.name,
            u'Collector'
        )
        service.idcollector = collector.idservice
        DBSession.flush()

        assert_equals(service.idcollector, collector.idservice)
        assert_equals(service.collector, collector)


class TestHighLevelService(ModelTest, TagTestMixin):
    """Test de la classe HighLevelService."""

    klass = HighLevelService
    attrs = {
        'servicename': u'myservice',
        'message': u'Hello world',
        'warning_threshold': 50,
        'critical_threshold': 80,
    }

    def test_by_service_name(self):
        """Récupération d'un HighLevelService par son nom."""
        ob = HighLevelService.by_service_name(self.attrs['servicename'])
        assert_equals(ob.critical_threshold, 80)

    def test_default_state(self):
        """L'état initial d'un service de haut niveau est 'UNKNOWN'."""
        assert_equals(u'UNKNOWN', StateName.value_to_statename(
            DBSession.query(self.klass).one().state.state))


class TestSupItemAbstraction(unittest.TestCase):
    """
    Teste l'abstraction des hôtes/services
    en tant qu'éléments supervisés (SupItem).
    """

    def setUp(self):
        """Préparatifs pour les tests."""
        super(TestSupItemAbstraction, self).setUp()
        setup_db()

    def tearDown(self):
        """Nettoyage à l'issue des tests."""
        DBSession.rollback()
        DBSession.expunge_all()
        teardown_db()
        super(TestSupItemAbstraction, self).tearDown()

    def test_get_abstract_service(self):
        """Une interrogation sur Service ne doit pas retourner un Host."""
        functions.add_host(u'myhost')
        functions.add_highlevelservice(u'hls', message="foo")
        supitem = DBSession.query(Service).one()
        self.assertTrue(isinstance(supitem, HighLevelService))
