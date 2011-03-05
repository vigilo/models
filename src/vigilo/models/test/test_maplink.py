# -*- coding: utf-8 -*-
"""Test suite for LowLevelService & HighLevelService classes"""
from datetime import datetime

from vigilo.models.tables import Host, LowLevelService, Map, \
                            MapLlsLink, MapNodeHost
from vigilo.models.session import DBSession

from controller import ModelTest

class TestMapLlsLink(ModelTest):
    """Test de la classe MapLlsLink."""

    klass = MapLlsLink
    attrs = {}

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
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
        host1 = Host(
            name=u"host1.example.com",
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            description=u'Host 1',
            hosttpl=u'foo',
            address=u'127.0.0.1',
            snmpport=42,
            weight=42,
        )
        DBSession.add(host1)
        DBSession.flush()
        host2 = Host(
            name=u"host2.example.com",
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            description=u'Host 2',
            hosttpl=u'foo',
            address=u'127.0.0.2',
            snmpport=41,
            weight=41,
        )
        DBSession.add(host2)
        reference=LowLevelService(
            servicename=u'myservice',
            weight=100,
            host=host1,
        )
        from_node = MapNodeHost(label=u'Host 1',
            idmap=map.idmap,
            x_pos=220,
            y_pos=350,
            idhost=host1.idhost,
            icon=u'server',
        )
        to_node = MapNodeHost(label=u'Host 2',
            idmap=map.idmap,
            x_pos=220,
            y_pos=350,
            idhost=host1.idhost,
            icon=u'server',
        )
        DBSession.add(from_node)
        DBSession.add(to_node)
        DBSession.add(reference)
        DBSession.flush()
        return dict(from_node=from_node,
                    to_node=to_node,
                    map=map,
                    reference=reference)
