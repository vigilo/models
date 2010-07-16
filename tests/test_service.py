# -*- coding: utf-8 -*-
"""Test suite for LowLevelService & HighLevelService classes"""
from nose.tools import assert_equals

from vigilo.models.tables import Host, LowLevelService, HighLevelService, StateName
from vigilo.models.session import DBSession

from controller import ModelTest

class TestLowLevelService(ModelTest):
    """Test de la classe LowLevelService."""

    klass = LowLevelService
    attrs = {
        'servicename': u'myservice',
        'op_dep': u'+',
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
        assert_equals(u'OK', StateName.value_to_statename(
            DBSession.query(self.klass).one().state.state))
        

class TestHighLevelService(ModelTest):
    """Test de la classe HighLevelService."""

    klass = HighLevelService
    attrs = {
        'servicename': u'myservice',
        'op_dep': u'+',
        'message': u'Hello world',
        'warning_threshold': 50,
        'critical_threshold': 80,
        'priority': 1,
    }

    def __init__(self):
        ModelTest.__init__(self)

    def test_by_service_name(self):
        """Récupération d'un HighLevelService par son nom.'"""
        ob = HighLevelService.by_service_name(u'myservice')
        assert_equals(ob.critical_threshold, 80)

    def test_default_state(self):
        assert_equals(u'OK', StateName.value_to_statename(
            DBSession.query(self.klass).one().state.state))

