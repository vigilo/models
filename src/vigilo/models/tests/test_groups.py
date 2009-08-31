# -*- coding: utf-8 -*-
"""Test suite for Groups class"""
from vigilo.models import Groups
from vigilo.models.tests import ModelTest

class TestGroups(ModelTest):
    """Test de la table Groups"""

    klass = Groups
    attrs = dict(name = "mongroup")

