# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for LowLevelService & HighLevelService classes"""
import unittest
from nose.tools import assert_equals

from vigilo.models.tables import Host, Service, StateName, \
                                    LowLevelService, HighLevelService
from vigilo.models.session import DBSession
from vigilo.models.demo.functions import add_lowlevelservice
from test_tag import TagTestMixin

from controller import ModelTest, setup_db, teardown_db

class TestLowLevelService(ModelTest, TagTestMixin):
    """Test de la classe LowLevelService."""

    klass = LowLevelService
    attrs = {
        'servicename': u'myservice',
        'weight': 100,
    }

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        # Création de l'hôte physique sur lequel portera la dépendance.
        host = Host(
            name=u'myhost',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'foo',
            address=u'127.0.0.1',
            snmpport=42,
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()
        return dict(host=host)

    def test_by_host_service_name(self):
        """Récupération d'un LowLevelService par son nom d'hôte/service."""
        ob = LowLevelService.by_host_service_name(
            u'myhost', self.attrs['servicename'])
        assert_equals(ob.weight, 100)

    def test_default_state(self):
        """L'état initial d'un service de bas niveau est 'OK'."""
        assert_equals(u'OK', StateName.value_to_statename(
            DBSession.query(self.klass).one().state.state))

    def test_collector_relation(self):
        """Bon fonctionnement de l'association service -> collector."""
        service = DBSession.query(self.klass).one()
        collector = add_lowlevelservice(service.host.name, u'Collector')
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
        host = Host(
            name=u'myhost',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'foo',
            address=u'127.0.0.1',
            snmpport=42,
            weight=42,
        )
        DBSession.add(host)

        hls = HighLevelService(
            servicename=u'hls',
            message=u'foo',
            warning_threshold=42,
            critical_threshold=42,
        )
        DBSession.add(hls)
        DBSession.flush()

        supitem = DBSession.query(Service).one()
        self.assertTrue(isinstance(supitem, HighLevelService))
