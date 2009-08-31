# -*- coding: utf-8 -*-
"""Test suite for PerfDataSource class"""
from vigilo.models import Host, Service, Graph, PerfDataSource
from vigilo.models.tests import ModelTest

class TestPerfDataSource(ModelTest):
    """Test de la table perfdatasource"""

    klass = PerfDataSource
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(name = "monhost"))
        DBSession.add(Service(name = "monservice"))
        DBSession.add(Graph(name = "mongraph"))
        DBSession.flush()
        return dict(hostname = "monhost", servicename = "monservice",
                graphname = "mongraph")

