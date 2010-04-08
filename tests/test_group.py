# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
from nose.tools import assert_equal

from vigilo.models.session import DBSession
from vigilo.models.tables import GraphGroup, MapGroup, SupItemGroup
from vigilo.models.tables import GroupHierarchy

from controller import ModelTest

class TestMapGroup(ModelTest):
    """Test de la table MapGroup"""

    klass = MapGroup
    attrs = {
        'name': u'mapgroup'
    }

    def __init__(self):
        ModelTest.__init__(self)
        

class TestSupItemGroups(ModelTest):
    """Test de la table hostgroup"""

    klass = SupItemGroup
    attrs = {
        'name': u'hostgroup',
    }

    def __init__(self):
        ModelTest.__init__(self)
    
    def test_get_top_groups(self):
        """Test méthode get_top_groups"""
        assert_equal(self.obj, DBSession.query(SupItemGroup).first())

        DBSession.add(GroupHierarchy(
            parent=self.obj,
            child=self.obj,
            hops=0,
        ))
        DBSession.flush()

        tops = self.klass.get_top_groups()
        assert_equal(len(tops), 1)
        assert_equal(tops[0], self.obj)

class TestGraphGroup(ModelTest):
    """Test de la table GraphGroup"""

    klass = GraphGroup
    attrs = dict(name = u"mongraph")

    def __init__(self):
        ModelTest.__init__(self)

