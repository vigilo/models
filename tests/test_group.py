# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
from nose.tools import assert_equal

from vigilo.models.tables import ServiceGroup, GraphGroup, MapGroup, HostGroup
from vigilo.models.session import DBSession

from controller import ModelTest

class TestServiceGroup(ModelTest):
    """Test de la table ServiceGroup"""

    klass = ServiceGroup
    attrs = {
        'name': u'servicegroup'
    }

    def __init__(self):
        ModelTest.__init__(self)
        
        
class TestMapGroup(ModelTest):
    """Test de la table MapGroup"""

    klass = MapGroup
    attrs = {
        'name': u'mapgroup'
    }

    def __init__(self):
        ModelTest.__init__(self)
        

class TestHostGroups(ModelTest):
    """Test de la table hostgroup"""

    klass = HostGroup
    attrs = {
        'name': u'hostgroup',
    }

    def __init__(self):
        ModelTest.__init__(self)
    
    def test_get_top_groups(self):
        """Test méthode get_top_groups"""
        assert_equal(self.obj, DBSession.query(HostGroup).first())
        
        tops = self.klass.get_top_groups()
        assert_equal(len(tops), 1)
        assert_equal(tops[0], self.obj)
        
class TestGraphGroup(ModelTest):
    """Test de la table GraphGroup"""

    klass = GraphGroup
    attrs = dict(name = u"mongraph")

    def __init__(self):
        ModelTest.__init__(self)

