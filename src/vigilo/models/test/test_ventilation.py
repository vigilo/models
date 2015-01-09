# -*- coding: utf-8 -*-
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""Test suite for Ventilation class"""

from vigilo.models.test.controller import ModelTest
from vigilo.models.demo import functions
from vigilo.models.tables import Ventilation

class TestVentilation(ModelTest):
    """Test de la table Ventilation"""

    klass = Ventilation
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        vs = functions.add_vigiloserver(u'supserver.example.com')
        app = functions.add_application(u'app')

        return dict(host=host, vigiloserver=vs, application=app)

#    def test_query_obj(self):
#        """Vérifie les données insérées."""
#        super(TestVentilation, self).test_query_obj()
#        obj = DBSession.query(self.klass).one()
#
#        vserver = obj.vigiloserver
#        assert_equals(vserver.name, u'supserver1')
#        assert_equals(obj.host.name, u'myhost')
#        #assert_equals(obj.appgroup.name, u'appgroup1')
#        assert_equals(len(vserver.appgroups), 1)
#        assert_equals(vserver.appgroups[0].name, u'appgroup1')
