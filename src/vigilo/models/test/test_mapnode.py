# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for LowLevelService & HighLevelService classes"""
from datetime import datetime

from vigilo.models.tables import Host, LowLevelService, HighLevelService, \
        Map, MapNodeHost, MapNodeLls, MapNodeHls
from vigilo.models.session import DBSession

from controller import ModelTest

class TestMapNodeHost(ModelTest):
    """Test de la classe MapNodeHost."""

    klass = MapNodeHost
    attrs = {
        'label': u'Host 1',
        'x_pos': 220,
        'y_pos': 350,
        'icon': u'server',
        'minimize': True,
        }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        # Création des objets nécessaires  aux relations.
        new_map = Map(
                mtime=datetime.today(),
                title=u'Carte 1',
                background_color=u'#66FFFF',
                background_image=u'France',
                background_position=u'top right',
                background_repeat=u'no-repeat',
        )
        DBSession.add(new_map)
        DBSession.flush()
        host = Host(
            name=u"host1.example.com",
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            description=u'Host 1',
            hosttpl=u'foo',
            address=u'127.0.0.1',
            snmpport=42,
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()
        return dict(map=new_map, host=host)


class TestMapNodeLls(ModelTest):
    """Test de la classe MapNodeLls."""

    klass = MapNodeLls
    attrs = {
        'label': u'Service 1',
        'x_pos': 220,
        'y_pos': 350,
        'icon': u'server',
        'minimize': True,
        }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        # Création des objets nécessaires  aux relations.
        new_map = Map(
                mtime=datetime.today(),
                title=u'Carte 1',
                background_color=u'#66FFFF',
                background_image=u'France',
                background_position=u'top right',
                background_repeat=u'no-repeat',
        )
        DBSession.add(new_map)
        DBSession.flush()
        host = Host(
            name=u"host1.example.com",
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            description=u'Host 1',
            hosttpl=u'foo',
            address=u'127.0.0.1',
            snmpport=42,
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()
        service = LowLevelService(
            servicename=u'myservice',
            weight=100,
            host=host,
        )
        DBSession.add(service)
        DBSession.flush()
        return dict(map=new_map, service=service)


class TestMapNodeHls(ModelTest):
    """Test de la classe MapNodeHls."""

    klass = MapNodeHls
    attrs = {
        'label': u'Service 1',
        'x_pos': 220,
        'y_pos': 350,
        'icon': u'server',
        'minimize': True,
        }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        # Création des objets nécessaires  aux relations.
        new_map = Map(
                mtime=datetime.today(),
                title=u'Carte 1',
                background_color=u'#66FFFF',
                background_image=u'France',
                background_position=u'top right',
                background_repeat=u'no-repeat',
        )
        DBSession.add(new_map)
        DBSession.flush()
        host = Host(
            name=u"host1.example.com",
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            description=u'Host 1',
            hosttpl=u'foo',
            address=u'127.0.0.1',
            snmpport=42,
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()
        service = HighLevelService(
            servicename=u'myservice',
            message= u'Hello world',
            warning_threshold= 50,
            critical_threshold= 80,
        )
        DBSession.add(service)
        DBSession.flush()
        return dict(map=new_map, service=service)
