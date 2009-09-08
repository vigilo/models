# -*- coding: utf-8 -*-
"""Test suite for GraphGroups class"""
from vigilo.models import GraphGroups
from vigilo.models.tests import ModelTest

class TestGraphGroups(ModelTest):
    """Test de la table GraphGroups"""

    klass = GraphGroups
    attrs = dict(name = u"mongraph")

    def __init__(self):
        ModelTest.__init__(self)
