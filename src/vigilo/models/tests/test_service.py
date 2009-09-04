# -*- coding: utf-8 -*-
"""Test suite for Service class"""
from vigilo.models import Service
from vigilo.models.tests import ModelTest

class TestService(ModelTest):
    """Test de la table service"""

    klass = Service
    attrs = dict(name = u"monservice")

    def __init__(self):
        ModelTest.__init__(self)

