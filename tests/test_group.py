# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
from nose.tools import assert_equal

from vigilo.models.session import DBSession

from vigilo.models.tables import GraphGroup, MapGroup, SupItemGroup
from vigilo.models.tables import GroupHierarchy

from controller import ModelTest

class TestGroup(ModelTest):
    """Test de la table Group"""
    
    # Group est abstraite, on teste donc avec une classe dérivée
    klass = GraphGroup
    attrs = {
        'name': u'agroup'
    }

    def __init__(self):
        ModelTest.__init__(self)
    
    def test_remove_children(self):
        """ test méthode remove_children
        """
        child = self.klass(name=u"achild")
        DBSession.add(child)
        DBSession.add(GroupHierarchy(
            parent=self.obj,
            child=child,
            hops=1,
        ))
        DBSession.flush()
        
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.idparent == self.obj.idgroup
                        ).filter(GroupHierarchy.idchild == child.idgroup
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        
        self.obj.remove_children()
        
        assert_equal(0,
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.idparent == self.obj.idgroup
                        ).filter(GroupHierarchy.idchild == child.idgroup
                        ).filter(GroupHierarchy.hops == 1
                        ).count() )
        
    
    def test_has_parent(self):
        """ test méthode has_parent
        """
        assert_equal(self.obj.has_parent(), False)
        
        parent = self.klass(name=u"aparent")
        DBSession.add(parent)
        DBSession.add(GroupHierarchy(
            parent=parent,
            child=self.obj,
            hops=1,
        ))
        DBSession.flush()
        
        assert_equal(self.obj.has_parent(), True)
        
    
    def test_get_parent(self):
        """ test méthode get_parent
        """
        parent = self.klass(name=u"aparent")
        DBSession.add(parent)
        DBSession.add(GroupHierarchy(
            parent=parent,
            child=self.obj,
            hops=1,
        ))
        DBSession.flush()
        
        assert_equal(self.obj.get_parent(), parent)
        
    def test_set_parent(self):
        """ test méthode set_parent
        """
        parent = self.klass(name=u"aparent")
        DBSession.add(parent)
        
        self.obj.set_parent(parent)
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.idparent == parent.idgroup
                        ).filter(GroupHierarchy.idchild == self.obj.idgroup
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        
        anotherparent = self.klass(name=u"anotherparent")
        DBSession.add(anotherparent)
        
        self.obj.set_parent(anotherparent)
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.idparent == parent.idgroup
                        ).filter(GroupHierarchy.idchild == self.obj.idgroup
                        ).filter(GroupHierarchy.hops == 1
                        ).one()


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

