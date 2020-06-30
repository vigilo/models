# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Application class"""
from nose.tools import assert_equal
from vigilo.models.tables import Application

from vigilo.models.test.controller import ModelTest

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

