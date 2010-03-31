# -*- coding: utf-8 -*-
"""Test suite for EventHistory class"""
import re
from datetime import datetime
from nose.tools import assert_true

from vigilo.models.session import DBSession
from vigilo.models.tables import EventHistory, Host, LowLevelService, Event

from controller import ModelTest

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

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=1234,
            weight=42,
        )
        DBSession.add(host)

        service = LowLevelService(
            host=host,
            servicename=u'monservice',
            command=u'halt',
            op_dep=u'+',
            weight=42,
        )
        DBSession.add(service)
        DBSession.flush()

        DBSession.add(Event(
            idevent=42,
            timestamp=datetime.now(),
            supitem=service,
            current_state=u'OK',
            message=u'Foo',
            ))
        DBSession.flush()

        return dict(idevent=DBSession.query(Event.idevent)[0].idevent)

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

