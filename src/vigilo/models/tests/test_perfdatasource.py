# -*- coding: utf-8 -*-
"""Test suite for PerfDataSource class"""
from vigilo.models import Host, Service, Graph, PerfDataSource
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
            name=u'monhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            ))
        DBSession.add(Service(
            name=u'monservice',
            servicetype=u'foo',
            command=u'halt',
            ))
        DBSession.add(Graph(name = u"mongraph"))
        DBSession.flush()
        return dict(hostname = u"monhost", servicename = u"monservice",
                graphname = u"mongraph")

