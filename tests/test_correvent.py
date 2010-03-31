# -*- coding: utf-8 -*-
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
        'status': u'OK',
        'timestamp_active': datetime.now(),
        'priority': 0,
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
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()

        service = LowLevelService(
            host=host,
            servicename=u'myservice',
            command=u'halt',
            op_dep=u'+',
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
        form1 = re.compile("^\w* \w* \d*:\d*:\d*$")
        form2 = re.compile("^\w* \d*:\d*:\d*$")
        date = self.obj.get_date("timestamp_active")
        assert_true(form1.match(date) or form2.match(date))

    def test_get_since_date(self):
        """La fonction GetSinceDate doit renvoyer un objet formaté"""
        assert_true(re.compile("^\d*d \d*h \d'$").match(
            self.obj.get_since_date("timestamp_active")))

