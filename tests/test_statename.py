# -*- coding: utf-8 -*-
"""Test suite for StateName class"""
from nose.tools import assert_equals

from vigilo.models.tables import StateName
from vigilo.models.session import DBSession

from controller import ModelTest

class TestStateName(ModelTest):
    """Test de la table StateName."""

    klass = StateName
    attrs = {
        'statename': u'Foo',
        'order': 42,
    }

    def __init__(self):
        """Initialise le test."""
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """
        On surcharge la méthode de ModelTest
        car elle insère déjà des noms d'états.
        On veut éviter toute interférence dans les tests.
        """
        # On n'appelle pas le parent car ici
        # on ne VEUT PAS que des StateName
        # soient insérés par défaut.
        return {}

    def test_statename_to_value(self):
        """Teste la récupération d'une valeur d'état par son nom."""
        # Si on parvient à récupérer une information sans erreurs,
        # alors le test est concluant.
        self.obj.statename_to_value(u'Foo')

    def test_value_to_statename(self):
        """Teste la récupération d'un nom d'état par sa valeur."""
        row = DBSession.query(StateName.idstatename).first()
        statename = self.klass.value_to_statename(row.idstatename)
        assert_equals(u'Foo', statename)

    def test_cache(self):
        """Teste le cache des noms d'états."""
        row = DBSession.query(StateName).first()
        oldname = self.klass.value_to_statename(row.idstatename)
        row.statename = row.statename + u'_'
        DBSession.add(row)
        DBSession.flush()

        # On s'assure que le cache est bien utilisé :
        # ie. il renvoie l'ancien nom de l'état.
        currname = self.klass.value_to_statename(row.idstatename)
        assert_equals(oldname, currname)

        # De la même manière, le mapping inverse
        # fonctionne toujours avec l'ancien nom.
        assert_equals(row.idstatename, self.klass.statename_to_value(oldname))

        # On provoque un rafraîchissement du cache.
        assert_equals(row.idstatename, self.klass.statename_to_value(row.statename))
        try:
            self.klass.statename_to_value(oldname)
        except:
            pass
        else:
            raise AssertionError, "The cache was not refreshed"
