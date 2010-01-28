# -*- coding: utf-8 -*-
"""Test suite for Ventilation class"""
from nose.tools import assert_equals

from vigilo.models import Ventilation, Host, VigiloServer, Application
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
        DBSession.add(Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        ))
        
        vserver = VigiloServer(
           name=u'supserver1',
           description=u'a vigilo server'
        )
        DBSession.add(vserver)
        
        app = Application(
           name=u'app',
        )
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

