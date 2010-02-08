# -*- coding: utf-8 -*-
"""Test suite for LowLevelService & HighLevelService classes"""
from vigilo.models import Host, LowLevelService, HighLevelService
from vigilo.models.configure import DBSession

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
        # Création de l'hôte physique sur lequel portera la dépendance.
        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'foo',
            mainip=u'127.0.0.1',
            snmpport=42,
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()
        return dict(host=host)

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

