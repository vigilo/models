# -*- coding: utf-8 -*-
"""Test suite for PerfDataSource class"""
from vigilo.models.tables import PerfDataSource
from vigilo.models.demo import functions

from controller import ModelTest

class TestPerfDataSource(ModelTest):
    """Test de la table perfdatasource"""

    klass = PerfDataSource
    attrs = {
        'name': u'myperfsource',
    }

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        return dict(host=host)
