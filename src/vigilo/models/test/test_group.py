# -*- coding: utf-8 -*-
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for ServiceGroup class"""

import string

from nose.tools import assert_equal
from sqlalchemy.schema import DDL

from vigilo.models.session import DBSession
from vigilo.models.tables import GraphGroup, MapGroup, SupItemGroup
from vigilo.models.tables.grouphierarchy import GroupHierarchy
from vigilo.models.demo.functions import add_graphgroup, \
                                        add_supitemgroup, \
                                        add_mapgroup, add_map

from vigilo.models.test.controller import ModelTest

class TestGraphGroup(ModelTest):
    """Test de la table GraphGroup"""

    # Group est abstraite, on teste donc avec une classe dérivée
    klass = GraphGroup
    creator = add_graphgroup
    attrs = {
        'name': u'graphgroup',
        'parent': None,
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
        """
        Test la méthode remove_children
        """
        # Ce hack est nécessaire lors du passage des tests unitaires
        # avec sqlite3. Il permet de simuler un ON DELETE CASCADE,
        # car cette fonctionnalité n'est pas présente dans les anciennes
        # version de sqlite.
        trigger = DDL(
            """
CREATE TRIGGER foobar
BEFORE DELETE ON %(group)s
FOR EACH ROW BEGIN
    DELETE FROM %(grouphierarchy)s
        WHERE %(grouphierarchy)s.idparent = OLD.idgroup;
    DELETE FROM %(grouphierarchy)s
        WHERE %(grouphierarchy)s.idchild = OLD.idgroup;
END;
            """,
            on='sqlite',
            context={
                'group': self.klass.__tablename__,
                'grouphierarchy': GroupHierarchy.__tablename__,
            }
        )
        DBSession.bind.execute(trigger)

        child = self.klass(name=u"achild", parent=self.obj)
        DBSession.add(child)
        DBSession.flush()

        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.idparent == self.obj.idgroup
                        ).filter(GroupHierarchy.idchild == child.idgroup
                        ).filter(GroupHierarchy.hops == 1
                        ).one()

        self.obj.remove_children()
        assert_equal(False, self.obj.has_children())

        assert_equal(0,
            DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.idparent == self.obj.idgroup
                        ).filter(GroupHierarchy.hops > 0
                        ).count() )

    def test_parent(self):
        """Affectation d'un parent à un groupe."""
        # Au début, nous n'avons pas de parent.
        assert_equal(self.obj.has_parent(), False)

        # On obtient un parent.
        parent = self.klass(name=u"aparent", parent=None)
        DBSession.add(parent)
        self.obj.parent = parent
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == parent
                        ).filter(GroupHierarchy.child == self.obj
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        assert_equal(self.obj.parent, parent)
        assert_equal(self.obj.has_parent(), True)

        # Notre parent est modifié.
        anotherparent = self.klass(name=u"anotherparent", parent=None)
        DBSession.add(anotherparent)
        self.obj.parent = anotherparent
        DBSession.query(GroupHierarchy
                        ).filter(GroupHierarchy.parent == anotherparent
                        ).filter(GroupHierarchy.child == self.obj
                        ).filter(GroupHierarchy.hops == 1
                        ).one()
        assert_equal(self.obj.parent, anotherparent)
        assert_equal(self.obj.has_parent(), True)

        # Suppression du parent.
        self.obj.parent = None
        assert_equal(self.obj.parent, None)
        assert_equal(self.obj.has_parent(), False)

    def test_set_parent2(self):
        """Affectation d'un parent avec hiérarchies coté enfant et parent."""
        # on créé un parent sur self.obj
        parent = self.klass(name=u"aparent", parent=None)
        DBSession.add(parent)
        self.obj.parent = parent

        # on créé un groupe avec son enfant
        child = self.klass(name=u"achild", parent=None)
        DBSession.add(child)
        gchild = self.klass(name=u"agrandchild", parent=None)
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

    def test_get_children_order(self):
        """La fonction get_children doit trier par ordre alphabétique"""
        names = [ u"achild_%s" % chr(c) for c in range(ord('a'), ord('z')) ]
        reversed_names = names[:]
        reversed_names.reverse()
        for name in reversed_names:
            child = self.klass(name=name)
            DBSession.add(child)
            DBSession.add(GroupHierarchy(
                parent=self.obj,
                child=child,
                hops=1,
            ))
        DBSession.flush()
        assert_equal( names, [ c.name for c in self.obj.get_children() ] )

    def test_get_children_limit(self):
        """L'option limit de get_children doit limiter le nombre retourné"""
        for i in range(10):
            child = self.klass(name=u"achild%d" % i)
            DBSession.add(child)
            DBSession.add(GroupHierarchy(
                parent=self.obj,
                child=child,
                hops=1,
            ))
        DBSession.flush()
        assert_equal( 5, len(self.obj.get_children(limit=5)) )

    def test_get_children_offset(self):
        """L'option offset de get_children doit décaler le résultat"""
        # on créé en ordre inverse pour tester le tri aussi
        names = [ u"achild%d" % i for i in range(9, 0, -1) ]
        for name in names:
            child = self.klass(name=name)
            DBSession.add(child)
            DBSession.add(GroupHierarchy(
                parent=self.obj,
                child=child,
                hops=1,
            ))
        DBSession.flush()
        names.reverse() # get_children va trier
        result_names = [ c.name for c in self.obj.get_children(offset=5) ]
        assert_equal(names[5:], result_names)

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

    def test_path(self):
        """Génération d'un chemin absolu vers le groupe."""
        root = self.creator.im_func(u'TestRoot', None)
        c1 = self.creator.im_func(u'/', root)
        c2 = self.creator.im_func(u'\\', c1)
        assert_equal(c2.path, u'/TestRoot/\\//\\\\')

    def test_by_path(self):
        """Récupération des groupes par leur chemin."""
        root = self.creator.im_func(u'Test', None)
        c1 = self.creator.im_func(u'Test', root)
        c2 = self.creator.im_func(u'Test', c1)

        assert_equal(root, self.klass.by_path(u'/Test'))
        assert_equal(c1, self.klass.by_path(u'/Test/Test'))
        assert_equal(c2, self.klass.by_path(u'/Test/Test/Test'))

# On reprend les tests de GraphGroup.
class TestMapGroup(TestGraphGroup):
    """Test de la table MapGroup"""

    klass = MapGroup
    creator = add_mapgroup
    attrs = {
        'name': u'mapgroup',
        'parent': None,
    }

    def test_get_maps(self):
        """La fonction get_maps doit récupérer les cartes du groupe"""
        # on créé en ordre inverse pour tester le tri
        titles = [ u"test_map_%d" % i for i in range(9, 0, -1) ]
        for title in titles:
            add_map(title, self.obj)
        DBSession.flush()
        titles.reverse() # get_maps va trier
        result_titles = [ c.title for c in self.obj.get_maps() ]
        assert_equal(titles, result_titles)

    def test_get_maps_limit(self):
        """La fonction get_maps doit récupérer les cartes du groupe"""
        titles = [ u"test_map_%d" % i for i in range(10) ]
        for title in titles:
            add_map(title, self.obj)
        DBSession.flush()
        assert_equal(5, len(self.obj.get_maps(limit=5)))

    def test_get_maps_offset(self):
        """L'option offset de get_maps doit décaler le résultat"""
        # on créé en ordre inverse pour tester le tri aussi
        titles = [ u"test_map_%d" % i for i in range(9, 0, -1) ]
        for title in titles:
            add_map(title, self.obj)
        DBSession.flush()
        titles.reverse() # get_maps va trier
        result_titles = [ c.title for c in self.obj.get_maps(offset=5) ]
        assert_equal(titles[5:], result_titles)


class TestSupItemGroups(TestGraphGroup):
    """Test de la table SupItemGroup"""

    klass = SupItemGroup
    creator = add_supitemgroup
    attrs = {
        'name': u'supitemgroup',
        'parent': None,
    }
