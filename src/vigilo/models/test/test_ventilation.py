# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Ventilation class"""
from nose.tools import assert_equals

from vigilo.models.tables import Ventilation, Host, VigiloServer, Application
from vigilo.models.session import DBSession

from controller import ModelTest

class TestVentilation(ModelTest):
    """Test de la table Ventilation"""

    klass = Ventilation
    attrs = {}

    def __init__(self):
        ModelTest.__init__(self)
    
    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        DBSession.add(Host(
            name=u'myhost',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            address=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        ))
        
        vserver = VigiloServer(name=u'supserver.example.com')
        DBSession.add(vserver)
        
        app = Application(name=u'app')
        DBSession.add(app)

        DBSession.flush()
        return dict(
            host=DBSession.query(Host).first(),
            vigiloserver=DBSession.query(VigiloServer).first(),
            application=DBSession.query(Application).first()
        )

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

