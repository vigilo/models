# -*- coding: utf-8 -*-
"""Test suite for PerfDataSource class"""
from vigilo.models import Host, Service, Graph, PerfDataSource
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestPerfDataSource(ModelTest):
    """Test de la table perfdatasource"""

    klass = PerfDataSource
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(name = u"monhost"))
        DBSession.add(Service(name = u"monservice"))
        DBSession.add(Graph(name = u"mongraph"))
        DBSession.flush()
        return dict(hostname = u"monhost", servicename = u"monservice",
                graphname = u"mongraph")

