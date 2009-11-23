# -*- coding: utf-8 -*-
"""Test suite for PerfDataSource class"""
from vigilo.models import Host, ServiceLowLevel, Graph, PerfDataSource
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestPerfDataSource(ModelTest):
    """Test de la table perfdatasource"""

    klass = PerfDataSource
    attrs = {}

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(
            hostname=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
        ))

        service = ServiceLowLevel(
            hostname=u'myhost',
            servicename=u'myservice',
            command=u'halt',
            op_dep=u'+',
            priority=1,
        )
        DBSession.add(service)
        DBSession.flush()
        return dict(service=service)

