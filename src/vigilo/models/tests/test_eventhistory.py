# -*- coding: utf-8 -*-
"""Test suite for EventHistory class"""
from vigilo.models import EventHistory, Host, Service, Event
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from datetime import datetime

class TestEventHistory(ModelTest):
    """Test de la table EventHistory"""

    klass = EventHistory
    attrs = dict(type_action = u'Nagios update state', value = u'',
            text = u'', username = u'manager')

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

        DBSession.add(Event(
            idevent=u'foo',
            timestamp=datetime.now(),
            hostname=u'monhost',
            servicename=u'monservice',
            state=u'OK',
            message=u'Foo',
            ))
        DBSession.flush()

        return dict(idevent = DBSession.query(Event.idevent)[0].idevent)

