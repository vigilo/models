# -*- coding: utf-8 -*-
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for ImpactedHLS class"""
from vigilo.models.tables import ImpactedHLS, ImpactedPath
from vigilo.models.demo import functions
from vigilo.models.session import DBSession

from vigilo.models.test.controller import ModelTest

class TestImpactedHLS(ModelTest):
    """Unit test case for the ``ImpactedHLS`` model."""

    klass = ImpactedHLS
    attrs = {
        'distance': 42,
    }

    def do_get_dependencies(self):
        """Création des dépendances du test."""
        ModelTest.do_get_dependencies(self)
        hls = functions.add_highlevelservice(u'HLS')
        host = functions.add_host(u'myhost')
        path = ImpactedPath(supitem=host)
        DBSession.add(path)
        DBSession.flush()
        return dict(path=path, hls=hls)
