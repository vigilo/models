# -*- coding: utf-8 -*-
"""Test suite for ServiceLowLevel & ServiceHighLevel classes"""
from vigilo.models import ServiceLowLevel, ServiceHighLevel
from vigilo.models.tests import ModelTest

class TestServiceLowLevel(ModelTest):
    """Test de la classe ServiceLowLevel."""

    klass = ServiceLowLevel
    attrs = {
        'name': u'monservice',
        'op_dep': u'+',
    }

    def __init__(self):
        ModelTest.__init__(self)

class TestServiceHighLevel(ModelTest):
    """Test de la classe ServiceHighLevel."""

    klass = ServiceHighLevel
    attrs = {
        'name': u'monservice',
        'op_dep': u'+',
        'message': u'Hello world',
        'warning_threshold': 50,
        'critical_threshold': 80,
    }

    def __init__(self):
        ModelTest.__init__(self)

