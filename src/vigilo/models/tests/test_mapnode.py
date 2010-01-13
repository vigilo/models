# -*- coding: utf-8 -*-
"""Test suite for ServiceLowLevel & ServiceHighLevel classes"""
from vigilo.models import Host, ServiceLowLevel, Map, MapNodeHost
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from datetime import datetime

class TestMapNodeHost(ModelTest):
    """Test de la classe MapNodeHost."""

    klass = MapNodeHost
    attrs = {
        'label': u'Host 1', 
        'x_pos': 220, 
        'y_pos': 350, 
        'hosticon': u'server',
        'minimize': True,
        }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        # Création des objets nécessaires  aux relations.
        map = Map(
                mtime=datetime.today(),
                title=u'Carte 1',
                background_color=u'#66FFFF',
                background_image=u'France',
                background_position=u'top right',
                background_repeat=u'no-repeat',
        )
        DBSession.add(map)
        DBSession.flush()
        host = Host(
            name=u"host1.example.com",
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            description=u'Host 1',
            hosttpl=u'foo',
            mainip=u'127.0.0.1',
            snmpport=42,
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()
        service=ServiceLowLevel(
            servicename=u'myservice',
            op_dep=u'+',
            weight=100,
            host=host,
        )
        DBSession.add(service)
        DBSession.flush()
        return dict(map=map,
#                    service=service,
                    host=host)



