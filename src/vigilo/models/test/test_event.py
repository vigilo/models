# -*- coding: utf-8 -*-
# Copyright (C) 2006-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Event class"""
import re
from datetime import datetime
from nose.tools import assert_true, assert_equal

from vigilo.models.demo import functions
from vigilo.models.tables import Event, StateName

from vigilo.models.test.controller import ModelTest

class TestEvent(ModelTest):
    """Test de la table Event"""

    klass = Event
    attrs = {
        'idevent': 42,
        'timestamp': datetime.now(),
        # On ne peut pas utiliser StateName.statename_to_value ici
        # car le modèle n'est pas encore créé lorsque ce code est
        # exécuté.
        'current_state': 3, # = WARNING
        'message': u'Foo',
    }

    def do_get_dependencies(self):
        """Generate some data for the test"""
        # Insère les noms d'états dans la base de données.
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        service = functions.add_lowlevelservice(host, u'myservice')
        return dict(supitem=service)

    def test_get_date(self):
        """La fonction GetDate doit renvoyer un objet formaté"""
        # Motif pour une date du type "Mar 15, 2011 2:44:21 PM".
        form1 = re.compile("^\w* \d{1,2}, \d{4} \d{1,2}:\d{1,2}:\d{1,2} [PA]M$")
        result = self.obj.get_date("timestamp", "en")
        assert_true(form1.match(result))

    def test_get_since_date(self):
        """La fonction GetSinceDate doit renvoyer un objet formaté"""
        assert_true(re.compile("^\d*d \d*h \d'$").match(
            self.obj.get_since_date("timestamp", "en")))

    def test_initial_states(self):
        """Vérifie que l'état initial est celui attendu."""
        assert_equal(u'WARNING',
            StateName.value_to_statename(self.obj.initial_state),
            "The initial state should have been 'WARNING', got %r." %
            StateName.value_to_statename(self.obj.initial_state))

        assert_equal(u'WARNING',
            StateName.value_to_statename(self.obj.peak_state),
            "The peak state should have been 'WARNING', got %r." %
            StateName.value_to_statename(self.obj.peak_state))

    def test_read_only_states(self):
        """Les états initiaux/maximaux ne sont accessibles qu'en lecture."""
        # Tente de modifier l'état initial.
        try:
            self.obj.initial_state = \
                StateName.statename_to_value(u'CRITICAL')
        except AttributeError:
            pass
        state = StateName.value_to_statename(self.obj.initial_state)
        assert_equal(u'WARNING', state,
            "Expected initial state = 'WARNING', got %r." % state)

        # Force l'état maximal à 'CRITICAL'.
        self.obj.current_state = StateName.statename_to_value(u'CRITICAL')
        # Tente de repasser l'état maximal à 'UNKNOWN'.
        try:
            self.obj.peak_state = StateName.statename_to_value(u'UNKNOWN')
        except AttributeError:
            pass
        state = StateName.value_to_statename(self.obj.peak_state)
        assert_equal(u'CRITICAL', state,
            "Expected peak state = 'CRITICAL', got %r." % state)

    def test_peak_state(self):
        """Le pire état est automatiquement calculé et mis à jour."""
        assert_equal(u'WARNING',
            StateName.value_to_statename(self.obj.peak_state),
            "The peak state should have been 'WARNING', got %r." %
            StateName.value_to_statename(self.obj.peak_state))

        # L'état courant passe à 'CRITICAL' -> le pire état devient 'CRITICAL'.
        self.obj.current_state = StateName.statename_to_value(u'CRITICAL')

        assert_equal(u'CRITICAL',
            StateName.value_to_statename(self.obj.peak_state),
            "The peak state should have been 'CRITICAL', got %r." %
            StateName.value_to_statename(self.obj.peak_state))

        # L'état courant passe à 'OK' -> le pire état reste 'CRITICAL'.
        self.obj.current_state = StateName.statename_to_value(u'OK')

        assert_equal(u'CRITICAL',
            StateName.value_to_statename(self.obj.peak_state),
            "The peak state should have been 'CRITICAL', got %r." %
            StateName.value_to_statename(self.obj.peak_state))
