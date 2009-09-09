# -*- coding: utf-8 -*-
"""Test suite for Group class"""
from vigilo.models import Group
from vigilo.models.tests import ModelTest

class TestGroup(ModelTest):
    """Test de la table Group"""

    klass = Group
    attrs = dict(name = u"mongroup")

    def __init__(self):
        ModelTest.__init__(self)

