# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for the CorrEvent class"""
from nose.tools import assert_true
from datetime import datetime
import re

from vigilo.models.session import DBSession
from vigilo.models.tables import CorrEvent, Event, LowLevelService, Host
from controller import ModelTest

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
        host = Host(
            name=u'myhost',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            address=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()

        service = LowLevelService(
            host=host,
            servicename=u'myservice',
            command=u'halt',
            weight=42,
        )
        DBSession.add(service)

        DBSession.add(Event(
            timestamp=datetime.now(),
            supitem=service,
            current_state=u'OK',
            message=u'Foo',
            ))
        DBSession.flush()

        return dict(idcause=DBSession.query(Event).first().idevent)

    def test_get_date(self):
        """La fonction GetDate doit renvoyer un objet formaté"""
        # Motif pour une date du type "Mar 15, 2011 2:44:21 PM".
        form1 = re.compile("^\w* \d{1,2}, \d{4} \d{1,2}:\d{1,2}:\d{1,2} [PA]M$")
        result = self.obj.get_date("timestamp_active", "en")
        assert_true(form1.match(result))

    def test_get_since_date(self):
        """La fonction GetSinceDate doit renvoyer un objet formaté"""
        assert_true(re.compile("^\d*d \d*h \d'$").match(
            self.obj.get_since_date("timestamp_active", "en")))
