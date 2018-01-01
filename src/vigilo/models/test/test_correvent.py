# -*- coding: utf-8 -*-
# Copyright (C) 2006-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for the CorrEvent class"""
from nose.tools import assert_true
from datetime import datetime
import re

from vigilo.models.demo import functions
from vigilo.models.tables import CorrEvent
from vigilo.models.test.controller import ModelTest

class TestCorrEvent(ModelTest):
    """Test de la table CorrEvent"""

    klass = CorrEvent
    attrs = {
        'ack': CorrEvent.ACK_NONE,
        'timestamp_active': datetime.now(),
        'priority': 0,
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        service = functions.add_lowlevelservice(host, u'myservice')
        event = functions.add_event(service, u'OK', u'Foo')
        return dict(idcause=event.idevent)

    def test_get_date(self):
        """La fonction GetDate doit renvoyer un objet formaté"""
        # Exemples de résultats attendus (selon la version de Babel) :
        # Nov 12, 2013 8:43:40 PM
        # Nov 12, 2013, 8:43:40 PM
        pattern = re.compile("^\w{3} \d{1,2}, \d{4},? \d+:\d+:\d+ [AP]M$")
        result = self.obj.get_date("timestamp_active", "en")
        assert_true(pattern.match(result))

    def test_get_since_date(self):
        """La fonction GetSinceDate doit renvoyer un objet formaté"""
        assert_true(re.compile("^\d*d \d*h \d'$").match(
            self.obj.get_since_date("timestamp_active", "en")))
