# -*- coding: utf-8 -*-
"""Test suite for Event class"""
from vigilo.models import Event, Host, ServiceLowLevel, StateName
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_true, assert_equal
import re
from datetime import datetime

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

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        # Insère les noms d'états dans la base de données.
        ModelTest.do_get_dependencies(self)

        DBSession.add(Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=1234,
        ))

        service = ServiceLowLevel(
            hostname=u'myhost',
            servicename=u'myservice',
            command=u'halt',
            op_dep=u'+',
            priority=1,
        )
        DBSession.add(service)
        DBSession.flush()
        return dict(service=service)

    def test_get_date(self):
        """La fonction GetDate doit renvoyer un objet formaté"""
        form1 = re.compile("^\w* \w* \d*:\d*:\d*$")
        form2 = re.compile("^\w* \d*:\d*:\d*$")
        assert_true(form1.match(self.obj.get_date("timestamp")) \
                or form2.match(self.obj.get_date("timestamp")))

    def test_get_since_date(self):
        """La fonction GetSinceDate doit renvoyer un objet formaté"""
        assert_true(re.compile("^\d*d \d*h \d'$").match(
            self.obj.get_since_date("timestamp")))

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

