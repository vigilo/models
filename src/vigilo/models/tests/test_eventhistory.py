# -*- coding: utf-8 -*-
"""Test suite for EventHistory class"""
from vigilo.models import EventHistory, Host, ServiceLowLevel, Event
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from datetime import datetime

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

        DBSession.add(Host(
            hostname=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=1234,
        ))

        service = ServiceLowLevel(
            hostname=u'myhost',
            servicename=u'monservice',
            command=u'halt',
            op_dep=u'+',
            priority=1,
        )
        DBSession.add(service)
        DBSession.flush()

        DBSession.add(Event(
            idevent=42,
            timestamp=datetime.now(),
            service=service,
            current_state=u'OK',
            message=u'Foo',
            ))
        DBSession.flush()

        return dict(idevent=DBSession.query(Event.idevent)[0].idevent)

