# -*- coding: utf-8 -*-
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for LowLevelService & HighLevelService classes"""

from vigilo.models.tables import MapLlsLink
from vigilo.models.demo import functions

from vigilo.models.test.controller import ModelTest

class TestMapLlsLink(ModelTest):
    """Test de la classe MapLlsLink."""

    klass = MapLlsLink
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)

        # Création du groupe de cartes racine.
        functions.add_mapgroup(u'Root')

        # Création des objets nécessaires  aux relations.
        new_map = functions.add_map(u'Carte 1')
        host1 = functions.add_host(u'host1.example.com')
        host2 = functions.add_host(u'host2.example.com')
        reference = functions.add_lowlevelservice(host1, u'myservice')
        from_node = functions.add_node_host(host1, u'Host 1', new_map)
        to_node = functions.add_node_host(host2, u'Host 2', new_map)
        return dict(from_node=from_node,
                    to_node=to_node,
                    map=new_map,
                    reference=reference)
