# -*- coding: utf-8 -*-
"""Test suite for LowLevelService & HighLevelService classes"""
import unittest
from nose.tools import assert_equals

from vigilo.models.tables import Host, Service, StateName, \
                                    LowLevelService, HighLevelService
from vigilo.models.session import DBSession
from vigilo.models.demo.functions import add_lowlevelservice

from controller import ModelTest, setup_db, teardown_db

class TestLowLevelService(ModelTest):
    """Test de la classe LowLevelService."""

    klass = LowLevelService
    attrs = {
        'servicename': u'myservice',
        'weight': 100,
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        # Création de l'hôte physique sur lequel portera la dépendance.
        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt',
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
        ob = LowLevelService.by_host_service_name(u'myhost', u'myservice')
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


class TestHighLevelService(ModelTest):
    """Test de la classe HighLevelService."""

    klass = HighLevelService
    attrs = {
        'servicename': u'myservice',
        'message': u'Hello world',
        'warning_threshold': 50,
        'critical_threshold': 80,
        'priority': 1,
    }

    def __init__(self):
        ModelTest.__init__(self)

    def test_by_service_name(self):
        """Récupération d'un HighLevelService par son nom."""
        ob = HighLevelService.by_service_name(u'myservice')
        assert_equals(ob.critical_threshold, 80)

    def test_default_state(self):
        """L'état initial d'un service de haut niveau est 'OK'."""
        assert_equals(u'OK', StateName.value_to_statename(
            DBSession.query(self.klass).one().state.state))

class TestSupItemAbstraction(unittest.TestCase):
    def setUp(self):
        super(TestSupItemAbstraction, self).setUp()
        setup_db()
        DBSession.add(StateName(statename=u'OK', order=1))
        DBSession.add(StateName(statename=u'UP', order=1))
        DBSession.flush()

    def tearDown(self):
        DBSession.rollback()
        DBSession.expunge_all()
        teardown_db()
        super(TestSupItemAbstraction, self).tearDown()

    def test_get_abstract_service(self):
        """Une interrogation sur Service ne doit pas retourner un Host"""
        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt',
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
            priority=42,
        )
        DBSession.add(hls)
        DBSession.flush()

        supitem = DBSession.query(Service).one()
        self.assertEqual(supitem._itemtype, 'highlevel')
