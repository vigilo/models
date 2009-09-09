# -*- coding: utf-8 -*-
"""Test suite for GraphGroup class"""
from vigilo.models import GraphGroup
from vigilo.models.tests import ModelTest

class TestGraphGroup(ModelTest):
    """Test de la table GraphGroup"""

    klass = GraphGroup
    attrs = dict(name = u"mongraph")

    def __init__(self):
        ModelTest.__init__(self)

