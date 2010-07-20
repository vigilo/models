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

    def test_creation_loop(self):
        """
        Ajout des boucles dans la hiérarchie lors de la création d'un groupe.
        """
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.idparent == self.obj.idgroup
                        ).filter(GroupHierarchy.idchild == self.obj.idgroup
                        ).filter(GroupHierarchy.hops == 0
                        ).one()
    
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

    def test_parent(self):
        """Affectation d'un parent à un groupe."""
        # Au début, nous n'avons pas de parent.
        assert_equal(self.obj.has_parent(), False)

        # On obtient un parent.
        parent = self.klass(name=u"aparent")
        DBSession.add(parent)
        self.obj.parent = parent
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == parent
                        ).filter(GroupHierarchy.child == self.obj
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        assert_equal(self.obj.get_parent(), parent)
        assert_equal(self.obj.has_parent(), True)

        # Notre parent est modifié.
        anotherparent = self.klass(name=u"anotherparent")
        DBSession.add(anotherparent)
        self.obj.parent = anotherparent
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == anotherparent
                        ).filter(GroupHierarchy.child == self.obj
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        assert_equal(self.obj.get_parent(), anotherparent)
        assert_equal(self.obj.has_parent(), True)

        # Suppression du parent.
        self.obj.parent = None
        assert_equal(self.obj.get_parent(), None)
        assert_equal(self.obj.has_parent(), False)

    def test_set_parent2(self):
        """Affectation d'un parent avec hiérarchies coté enfant et parent."""
        # on créé un parent sur self.obj
        parent = self.klass(name=u"aparent")
        DBSession.add(parent)
        self.obj.parent = parent
        
        # on créé un groupe avec son enfant
        child = self.klass(name=u"achild")
        DBSession.add(child)
        gchild = self.klass(name=u"agrandchild")
        DBSession.add(gchild)
        gchild.parent = child
        
        # on raccorde self.obj et l'enfant
        child.parent = self.obj

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
        """Récupération des groupes au sommet de la hiérarchie."""
        tops = self.klass.get_top_groups()
        assert_equal(len(tops), 1)
        assert_equal(tops[0], self.obj)

    def test_has_children(self):
        """Test de la présence de fils."""
        assert_equal( False, self.obj.has_children() )
        
        child = self.klass(name=u"achild")
        DBSession.add(child)
        DBSession.add(GroupHierarchy(
            parent=self.obj,
            child=child,
            hops=1,
        ))
        DBSession.flush()
        
        assert_equal( True, self.obj.has_children() )
    
    def test_get_children(self):
        """Récupération des groupes fils."""
        child = self.klass(name=u"achild")
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

    def test_get_path(self):
        """Génération d'un chemin absolu vers le groupe."""
        root = self.creator.im_func(u'TestRoot', None)
        c1 = self.creator.im_func(u'/', root)
        c2 = self.creator.im_func(u'\\', c1)

        assert_equal(c2.get_path(), u'/TestRoot/\\//\\\\')

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

