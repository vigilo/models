# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
from vigilo.models import ServiceGroup
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestServiceGroup(ModelTest):
    """Test de la table ServiceGroup"""

    klass = ServiceGroup
    attrs = {
        'name': u'servicegroup'
    }

    def __init__(self):
        ModelTest.__init__(self)

