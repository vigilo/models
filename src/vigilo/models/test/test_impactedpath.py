# -*- coding: utf-8 -*-
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for ImpactedPath class"""
from vigilo.models.tables import ImpactedPath
from vigilo.models.demo import functions

from vigilo.models.test.controller import ModelTest

class TestImpactedPath(ModelTest):
    """Unit test case for the ``ImpactedPath`` model."""

    klass = ImpactedPath
    attrs = {}

    def do_get_dependencies(self):
        """Création des dépendances du test."""
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        return dict(supitem=host)
