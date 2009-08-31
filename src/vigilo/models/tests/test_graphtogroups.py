# -*- coding: utf-8 -*-
"""Test suite for GraphToGroups class"""
from vigilo.models import GraphToGroups, Graph, GraphGroups
from vigilo.models.tests import ModelTest

class TestGraphToGroups(ModelTest):
    """Test de la table GraphToGroups"""

    klass = GraphToGroups
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Graph(name = "mongraph"))
        DBSession.add(GraphGroups(name = "mongraphgroup"))
        DBSession.flush()
        return dict(graphname = "mongraph", groupname = "mongraphgroup")

