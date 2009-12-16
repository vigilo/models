# -*- coding: utf-8 -*-
"""Test suite for PerfDataSource class"""
from vigilo.models import Host, ServiceLowLevel, Graph, PerfDataSource
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestPerfDataSource(ModelTest):
    """Test de la table perfdatasource"""

    klass = PerfDataSource
    attrs = {
        'name': u'myperfsource',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)

        service = ServiceLowLevel(
            host=host,
            servicename=u'myservice',
            command=u'halt',
            op_dep=u'+',
            weight=42,
        )
        DBSession.add(service)
        DBSession.flush()
        return dict(service=service)

