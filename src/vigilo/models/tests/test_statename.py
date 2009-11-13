# -*- coding: utf-8 -*-
"""Test suite for StateName class"""
from vigilo.models import StateName
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

from nose.tools import assert_equals
from datetime import datetime

class TestStateName(ModelTest):
    """Test de la table StateName."""

    klass = StateName
    attrs = {
        'statename': u'Foo',
        'order': 42,
    }

    def __init__(self):
        """Initialise le test."""
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """On surcharge juste la méthode de ModelTest."""
        return {}

