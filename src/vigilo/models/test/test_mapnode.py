# -*- coding: utf-8 -*-
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for LowLevelService & HighLevelService classes"""

from vigilo.models.tables import MapNodeHost, MapNodeLls, MapNodeHls
from vigilo.models.demo import functions

from vigilo.models.test.controller import ModelTest

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

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)

        # Création du groupe de cartes racine.
        functions.add_mapgroup(u'Root')

        # Création des objets nécessaires  aux relations.
        new_map = functions.add_map(u'Carte 1')
        host = functions.add_host(u'host1.example.com')
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

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)

        # Création du groupe de cartes racine.
        functions.add_mapgroup(u'Root')

        # Création des objets nécessaires aux relations.
        new_map = functions.add_map(u'Carte 1')
        host = functions.add_host(u'host1.example.com')
        service = functions.add_lowlevelservice(host, u'myservice')
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

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)

        # Création du groupe de cartes racine.
        functions.add_mapgroup(u'Root')

        # Création des objets nécessaires  aux relations.
        new_map = functions.add_map(u'Carte 1')
        service = functions.add_highlevelservice(u'myservice')
        return dict(map=new_map, service=service)
