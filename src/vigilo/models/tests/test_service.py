# -*- coding: utf-8 -*-
"""Test suite for ServiceLowLevel & ServiceHighLevel classes"""
from vigilo.models import Host, ServiceLowLevel, ServiceHighLevel
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestServiceLowLevel(ModelTest):
    """Test de la classe ServiceLowLevel."""

    klass = ServiceLowLevel
    attrs = {
        'servicename': u'myservice',
        'op_dep': u'+',
        'weight': 100,
        'priority': 1,
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        # Création de l'hôte physique sur lequel portera la dépendance.
        host = Host(
            hostname=u'myhost',
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'foo',
            mainip=u'127.0.0.1',
            snmpport=42,
        )
        DBSession.add(host)
        DBSession.flush()
        return dict(hostname=u'myhost')

class TestServiceHighLevel(ModelTest):
    """Test de la classe ServiceHighLevel."""

    klass = ServiceHighLevel
    attrs = {
        'servicename': u'myservice',
        'op_dep': u'+',
        'message': u'Hello world',
        'warning_threshold': 50,
        'critical_threshold': 80,
    }

    def __init__(self):
        ModelTest.__init__(self)

