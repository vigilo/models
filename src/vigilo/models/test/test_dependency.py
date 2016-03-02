# -*- coding: utf-8 -*-
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Dependency class"""
from vigilo.models.tables import Dependency
from vigilo.models.demo import functions

from vigilo.models.test.controller import ModelTest

class TestDependency(ModelTest):
    """Test de la table Dependency."""

    klass = Dependency

    attrs = {
        'weight': 42,
        'warning_weight': 24,
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        service = functions.add_lowlevelservice(host, u'myservice')
        depgroup = functions.add_dependency_group(
                        host, service, u'hls', u'+')

        return dict(
            idgroup=depgroup,
            supitem=service,
        )
