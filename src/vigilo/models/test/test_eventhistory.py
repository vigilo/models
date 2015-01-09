# -*- coding: utf-8 -*-
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for EventHistory class"""
import re
from datetime import datetime
from nose.tools import assert_true

from vigilo.models.demo import functions
from vigilo.models.tables import EventHistory

from vigilo.models.test.controller import ModelTest

class TestEventHistory(ModelTest):
    """Test de la table EventHistory"""

    klass = EventHistory
    attrs = {
        'type_action': u'Nagios update state',
        'value': u'',
        'text': u'',
        'username': u'manager',
        'timestamp': datetime.now(),
    }

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        service = functions.add_lowlevelservice(host, u'myservice')
        event = functions.add_event(service, u'OK', u'Foo')
        return dict(idevent=event.idevent)

    def test_get_date(self):
        """La fonction GetDate doit renvoyer un objet formaté"""
        # Exemple de résultat attendu : Nov 12, 2013 8:43:40 PM
        assert_true(re.compile("^\w{3} \d+, \d{4} \d+:\d+:\d+ \w+$").match(
            self.obj.get_date("timestamp", "en")))

    def test_get_since_date(self):
        """La fonction GetSinceDate doit renvoyer un objet formaté"""
        # Exemple de résultat attendu : 0d 0h 0'
        assert_true(re.compile("^\d+d \d+h \d+'$").match(
            self.obj.get_since_date("timestamp", "en")))
