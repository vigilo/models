# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
from nose.tools import assert_equal

from vigilo.models.session import DBSession

from vigilo.models.tables import GraphGroup, MapGroup, SupItemGroup
from vigilo.models.tables.grouphierarchy import GroupHierarchy
from vigilo.models.demo.functions import add_graphgroup, \
                                        add_supitemgroup, \
                                        add_mapgroup

from controller import ModelTest

class TestGraphGroup(ModelTest):
    """Test de la table GraphGroup"""
    
    # Group est abstraite, on teste donc avec une classe dérivée
    klass = GraphGroup
    creator = add_graphgroup
    attrs = {
        'name': u'graphgroup'
    }

    def setup(self):
        """Set up the fixture used to test the model."""
        try:
            print "Class being tested:", self.klass
            new_attrs = {}
            new_attrs.update(self.attrs)
            new_attrs.update(self.do_get_dependencies())
            self.obj = self.klass.create(**new_attrs)
            DBSession.add(self.obj)
            DBSession.flush()
            return self.obj
        except:
            DBSession.rollback()
            raise

    def test_create(self):
        """ test de la méthode Group.create
        """
        group = self.klass.create(u'a group')
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.idparent == group.idgroup
                        ).filter(GroupHierarchy.idchild == group.idgroup
                        ).filter(GroupHierarchy.hops == 0
                        ).one()
        child = self.klass.create(name=u'a child', parent=group)
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.idparent == group.idgroup
                        ).filter(GroupHierarchy.idchild == child.idgroup
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
    
    def test_remove_children(self):
        """ test méthode remove_children
        """
        child = self.klass.create(name=u"achild")
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

    def test_parent(self):
        """ test méthode set_parent
        """
        # Au début, nous n'avons pas de parent.
        assert_equal(self.obj.has_parent(), False)

        # On obtient un parent.
        parent = self.klass.create(name=u"aparent")
        self.obj.set_parent(parent)
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == parent
                        ).filter(GroupHierarchy.child == self.obj
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        assert_equal(self.obj.get_parent(), parent)
        assert_equal(self.obj.has_parent(), True)

        # Notre parent est modifié.
        anotherparent = self.klass.create(name=u"anotherparent")
        self.obj.set_parent(anotherparent)
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == anotherparent
                        ).filter(GroupHierarchy.child == self.obj
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        assert_equal(self.obj.get_parent(), anotherparent)
        assert_equal(self.obj.has_parent(), True)

        # Suppression du parent.
        self.obj.set_parent(None)
        assert_equal(self.obj.get_parent(), None)
        assert_equal(self.obj.has_parent(), False)

    def test_set_parent2(self):
        """ test méthode set_parent avec hiérarchies coté enfant et parent
        """
        # on créé un parent sur self.obj
        parent = self.klass.create(name=u"aparent")
        DBSession.add(parent)
        self.obj.set_parent(parent)
        
        # on créé un groupe avec son enfant
        child = self.klass.create(name=u"achild")
        gchild = self.klass.create(name=u"agrandchild")
        gchild.set_parent(child)
        
        # on raccorde self.obj et l'enfant
        child.set_parent(self.obj)

        # Vérifications superficielles.
        assert_equal(4, DBSession.query(GroupHierarchy).filter(
                            GroupHierarchy.hops == 0).count())
        assert_equal(3, DBSession.query(GroupHierarchy).filter(
                            GroupHierarchy.hops == 1).count())
        assert_equal(2, DBSession.query(GroupHierarchy).filter(
                            GroupHierarchy.hops == 2).count())
        assert_equal(1, DBSession.query(GroupHierarchy).filter(
                            GroupHierarchy.hops == 3).count())

        # Vérification détaillée d'une partie des liens.
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == child
                        ).filter(GroupHierarchy.child == gchild
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == parent
                        ).filter(GroupHierarchy.child == self.obj
                        ).filter(GroupHierarchy.hops == 1
                        ).one()

        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == parent
                        ).filter(GroupHierarchy.child == gchild
                        ).filter(GroupHierarchy.hops == 3
                        ).one()
        
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == self.obj
                        ).filter(GroupHierarchy.child == child
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == self.obj
                        ).filter(GroupHierarchy.child == gchild
                        ).filter(GroupHierarchy.hops == 2
                        ).one()

    def test_get_top_groups(self):
        """Test méthode get_top_groups"""
        tops = self.klass.get_top_groups()
        assert_equal(len(tops), 1)
        assert_equal(tops[0], self.obj)
        
    def test_has_children(self):
        """
        """
        assert_equal( False, self.obj.has_children() )
        
        child = self.klass.create(name=u"achild")
        DBSession.add(child)
        DBSession.add(GroupHierarchy(
            parent=self.obj,
            child=child,
            hops=1,
        ))
        DBSession.flush()
        
        assert_equal( True, self.obj.has_children() )
    
    def test_get_children(self):
        """
        """
        child = self.klass.create(name=u"achild")
        DBSession.add(child)
        DBSession.add(GroupHierarchy(
            parent=self.obj,
            child=child,
            hops=1,
        ))
        DBSession.flush()
        
        assert_equal( [child, ], self.obj.get_children() )

    def test_search_for_groups(self):
        """Teste la récupération de groupes par nom/parent."""
        root = self.creator.im_func(u'TestRoot', None)
        child = self.creator.im_func(u'TestChild', root)
        fake = self.creator.im_func(u'TestRoot', root)

        # Récupération de la racine.
        assert_equal(root, self.klass.by_parent_and_name(None, u'TestRoot'))
        # Récupération des enfants.
        assert_equal(child, self.klass.by_parent_and_name(root, u'TestChild'))
        assert_equal(fake, self.klass.by_parent_and_name(root, u'TestRoot'))

# On reprend les tests de GraphGroup.
class TestMapGroup(TestGraphGroup):
    """Test de la table MapGroup"""

    klass = MapGroup
    creator = add_mapgroup
    attrs = {
        'name': u'mapgroup'
    }

class TestSupItemGroups(TestGraphGroup):
    """Test de la table SupItemGroup"""

    klass = SupItemGroup
    creator = add_supitemgroup
    attrs = {
        'name': u'supitemgorup',
    }

