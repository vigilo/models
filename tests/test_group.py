# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
from nose.tools import assert_equal
from sqlalchemy.schema import DDL

from vigilo.models.session import DBSession
from vigilo.models.tables import GraphGroup, MapGroup, SupItemGroup
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

    def test_remove_children(self):
        """
        Test la méthode remove_children
        """
        child = self.klass(name=u"achild", parent=self.obj)
        DBSession.add(child)
        DBSession.flush()

        self.obj.remove_children()
        assert_equal(False, self.obj.has_children())

    def test_parent(self):
        """Affectation d'un parent à un groupe."""
        # Au début, nous n'avons pas de parent.
        assert_equal(self.obj.has_parent(), False)

        g1 = self.klass(name=u"g1", parent=self.obj)
        g2 = self.klass(name=u"g2", parent=self.obj)
        g11 = self.klass(name=u"g11", parent=g1)
        DBSession.add(g1)
        DBSession.add(g2)
        DBSession.add(g11)
        DBSession.flush()

        assert_equal(self.obj.parent, None)
        assert_equal(g1.parent, self.obj)
        assert_equal(g2.parent, self.obj)
        assert_equal(g11.parent, g1)

        assert_equal(self.obj.has_parent(), False)
        for obj in [g1, g2, g11]:
            assert_equal(obj.has_parent(), True)

        g11.parent = g2
        DBSession.flush()

        assert_equal(self.obj.parent, None)
        assert_equal(g1.parent, self.obj)
        assert_equal(g2.parent, self.obj)
        assert_equal(g11.parent, g2)

        assert_equal(self.obj.has_parent(), False)
        for obj in [g1, g2, g11]:
            assert_equal(obj.has_parent(), True)

    def test_get_top_groups(self):
        """Récupération des groupes au sommet de la hiérarchie."""
        tops = self.klass.get_top_groups()
        assert_equal(len(tops), 1)
        assert_equal(tops[0], self.obj)

        """Test de la présence de fils."""
    def test_has_children(self):
        assert_equal(False, self.obj.has_children())

        child = self.klass(name=u"achild", parent=self.obj)
        DBSession.add(child)
        DBSession.flush()
        assert_equal(True, self.obj.has_children())

    def test_get_children(self):
        """Récupération des groupes fils."""
        assert_equal([], self.obj.get_children())
        child = self.klass(name=u"achild", parent=self.obj)
        DBSession.add(child)
        DBSession.flush()
        assert_equal([child], self.obj.get_children())

    def test_search_for_groups(self):
        """Teste la récupération de groupes par nom et parent."""
        child = self.klass(name=u"achild", parent=self.obj)
        DBSession.add(child)

        fake = self.klass(name=self.attrs['name'], parent=self.obj)
        DBSession.add(fake)
        DBSession.flush()

        # Récupération de la racine.
        assert_equal(self.obj, self.klass.by_parent_and_name(
            None, self.attrs['name']))

        # Récupération des enfants.
        assert_equal(child, self.klass.by_parent_and_name(
            self.obj, u'achild'))
        assert_equal(fake, self.klass.by_parent_and_name(
            self.obj, self.attrs['name']))

    def test_get_path(self):
        """Génération d'un chemin absolu vers le groupe."""
        c1 = self.creator.im_func(u'/', self.obj)
        c1 = DBSession.query(self.klass).filter(self.klass.name == u'/').first()
        c2 = self.creator.im_func(u'\\', c1)
        print repr(DBSession.query(
                self.klass.name,
                self.klass.left,
                self.klass.right,
                self.klass.depth,
            ).all())
        assert_equal(c2.get_path(), u'/' + self.attrs['name'] + u'/\\//\\\\')

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
        'name': u'supitemgroup',
    }
