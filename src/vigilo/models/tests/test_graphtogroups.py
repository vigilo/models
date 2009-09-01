# -*- coding: utf-8 -*-
"""Test suite for GraphToGroups class"""
from vigilo.models import GraphToGroups, Graph, GraphGroups
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestGraphToGroups(ModelTest):
    """Test de la table GraphToGroups"""

    klass = GraphToGroups
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Graph(name = u"mongraph"))
        DBSession.add(GraphGroups(name = u"mongraphgroup"))
        DBSession.flush()
        return dict(graphname = u"mongraph", groupname = u"mongraphgroup")

