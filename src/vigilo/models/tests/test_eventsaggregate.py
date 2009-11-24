# -*- coding: utf-8 -*-
"""Test suite for EventsAggregate class"""
from vigilo.models import EventsAggregate, Event, ServiceLowLevel, Host
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_true
import re
from datetime import datetime

class TestEventsAggregate(ModelTest):
    """Test de la table Event"""

    klass = EventsAggregate
    attrs = {
        'idaggregate': 42,
        'status': u'OK',
        'timestamp_active': datetime.now(),
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        DBSession.add(Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
        ))
        DBSession.flush()

        service = ServiceLowLevel(
            hostname=u'myhost',
            servicename=u'myservice',
            command=u'halt',
            op_dep=u'+',
            priority=1,
        )
        DBSession.add(service)

        DBSession.add(Event(
            idevent=42,
            timestamp=datetime.now(),
            service=service,
            current_state=u'OK',
            message=u'Foo',
            ))
        DBSession.flush()

        return dict(idcause=u'42')

    def test_get_date(self):
        """La fonction GetDate doit renvoyer un objet formaté"""
        form1 = re.compile("^\w* \w* \d*:\d*:\d*$")
        form2 = re.compile("^\w* \d*:\d*:\d*$")
        date = self.obj.get_date("timestamp_active")
        assert_true(form1.match(date) or form2.match(date))

    def test_get_since_date(self):
        """La fonction GetSinceDate doit renvoyer un objet formaté"""
        assert_true(re.compile("^\d*d \d*h \d'$").match(
            self.obj.get_since_date("timestamp_active")))

