#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from vigilo.common.conf import settings
settings.load_module(__name__)

from controller import setup_db, teardown_db

from vigilo.models.session import DBSession
from vigilo.models.tables import Host, Service, StateName, \
     Map, MapNode, MapNodeHost, MapNodeService, MapNodeLls, MapNodeHls
from vigilo.models.demo.functions import add_map, add_host, add_node_host, \
     add_node_lls, add_lowlevelservice, add_node_hls, add_highlevelservice


class DeleteCascadeTest(unittest.TestCase):
    """Test Sample"""

    def setUp(self):
        """Call before every test case."""
        setup_db()
        DBSession.add(StateName(statename=u'OK', order=0))

    def tearDown(self):
        """Call after every test case."""
        teardown_db()

    def test_host_mapnode(self):
        """Suppression des mapnodes d'un host supprimé (#57)"""
        # Mettre localhost sur une carte
        h = add_host(u"localhost")
        testmap = add_map(u"Test map")
        mnh = add_node_host(h, "localhost", testmap)
        DBSession.flush()
        DBSession.delete(h)
        DBSession.flush()
        # On vérifie que la suppression de l'hôte a bien supprimé ses
        # représentations cartographiques
        mn_count = DBSession.query(MapNode).count()
        self.assertEquals(mn_count, 0)
        mnh_count = DBSession.query(MapNodeHost).count()
        self.assertEquals(mnh_count, 0)

    def test_lls_mapnode(self):
        """Suppression des mapnodes d'un lls supprimé (#57)"""
        # Mettre localhost sur une carte
        h = add_host(u"localhost")
        s = add_lowlevelservice(h, "testservice")
        testmap = add_map(u"Test map")
        mnh = add_node_lls(s, "testservice", testmap)
        DBSession.flush()
        DBSession.delete(s)
        DBSession.flush()
        # On vérifie que la suppression du lls a bien supprimé ses
        # représentations cartographiques
        mn_count = DBSession.query(MapNode).count()
        self.assertEquals(mn_count, 0)
        mns_count = DBSession.query(MapNodeService).count()
        self.assertEquals(mns_count, 0)
        mnlls_count = DBSession.query(MapNodeLls).count()
        self.assertEquals(mnlls_count, 0)

    def test_hls_mapnode(self):
        """Suppression des mapnodes d'un hls supprimé (#57)"""
        # Mettre localhost sur une carte
        h = add_host(u"localhost")
        s = add_highlevelservice("testservice")
        testmap = add_map(u"Test map")
        mnh = add_node_hls(s, "testservice", testmap)
        DBSession.flush()
        DBSession.delete(s)
        DBSession.flush()
        # On vérifie que la suppression du hls a bien supprimé ses
        # représentations cartographiques
        mn_count = DBSession.query(MapNode).count()
        self.assertEquals(mn_count, 0)
        mns_count = DBSession.query(MapNodeService).count()
        self.assertEquals(mns_count, 0)
        mnlls_count = DBSession.query(MapNodeHls).count()
        self.assertEquals(mnlls_count, 0)


if __name__ == '__main__':
    unittest.main()
