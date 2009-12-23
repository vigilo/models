# -*- coding: utf-8 -*-
"""Test suite for Application class"""
from nose.tools import assert_equal
from vigilo.models import Application
from vigilo.models.tests import ModelTest

class TestApplication(ModelTest):
    """Unit test case for the ``Application`` model."""

    klass = Application
    attrs = {
        'name': u'Nagios',
    }

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def test_getting_by_app_name(self):
        """Teste la récupération d'instance grâce au nom de l'application."""
        app = Application.by_app_name(u'Nagios')
        assert_equal(self.obj, app)

