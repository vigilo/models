# -*- coding: utf-8 -*-
"""Test suite for Event class"""
from vigilo.models import Event, Host, Service
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_true, assert_equal
import re
from datetime import datetime

class TestEvent(ModelTest):
    """Test de la table Event"""

    klass = Event
    attrs = {
        'idevent': u'foo',
        'timestamp': datetime.now(),
        'hostname': u'monhost',
        'state': u'WARNING',
        'message': u'Foo',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        DBSession.add(Host(
            name=u'monhost',
            checkhostcmd=u'halt -f',
            community=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            port=u'1234',
            ))
        DBSession.add(Service(
            name=u'monservice',
            servicetype=u'foo',
            command=u'halt',
            ))
        DBSession.flush()
        return dict(hostname=u"monhost", servicename=u"monservice")

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
        assert_equal(u'WARNING', self.obj.initial_state,
            "The initial state should have been 'WARNING'.")
        assert_equal(u'WARNING', self.obj.peak_state,
            "The peak state should have been 'WARNING'.")

    def test_state_change(self):
        """Vérifie que les changements d'états sont bien pris en compte."""
        # On vérifie qu'en passant de WARNING à CRITICAL,
        # l'état maximal est bien mis à jour.
        self.obj.state = u'CRITICAL'
        assert_equal(u'CRITICAL', self.obj.peak_state,
            "The peak state should have been 'CRITICAL'.")

        # On modifie l'état en utilisant les nombres plutôt que les noms.
        # 0 = u'OK' (cf. State.names_mapping).
        self.obj.numeric_current_state = 0
        assert_equal(u'OK', self.obj.state,
            "The current state should have been 'OK', but we got %r." %
            self.obj.state)

    def test_read_only_states(self):
        """Les états initiaux/maximaux ne sont accessibles qu'en lecture."""
        # Tente de modifier l'état initial.
        try:
            self.obj.initial_state = u'CRITICAL'
        except AttributeError:
            pass
        assert_equal(u'WARNING', self.obj.initial_state,
            "Expected initial state = 'WARNING', got %r." %
            self.obj.initial_state)

        # Force l'état maximal à 'CRITICAL'.
        self.obj.state = u'CRITICAL'
        # Tente de repasser l'état maximal à 'UNKNOWN'.
        try:
            self.obj.peak_state = u'UNKNOWN'
        except AttributeError:
            pass
        assert_equal(u'CRITICAL', self.obj.peak_state,
            "Expected peak state = 'CRITICAL', got %r." %
            self.obj.peak_state)

