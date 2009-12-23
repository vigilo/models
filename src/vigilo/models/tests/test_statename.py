# -*- coding: utf-8 -*-
"""Test suite for StateName class"""
from nose.tools import assert_equals
from vigilo.models import StateName
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

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
        return {}

    def test_statename_to_value(self):
        """Teste la récupération d'une valeur d'état par son nom."""
        # Si on parvient à récupérer une information sans erreurs,
        # alors le test est concluant.
        self.obj.statename_to_value(u'Foo')

    def test_value_to_statename(self):
        """Teste la récupération d'un nom d'état par sa valeur."""
        row = DBSession.query(StateName.idstatename).first()
        statename = self.obj.value_to_statename(row.idstatename)
        assert_equals(u'Foo', statename)

