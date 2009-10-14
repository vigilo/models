# -*- coding: utf-8 -*-
"""Test suite for Event class"""
from vigilo.models import Event, Host, Service
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_true
import re
from datetime import datetime

class TestEvent(ModelTest):
    """Test de la table Event"""

    klass = Event
    attrs = {
        'idevent': u'foo',
        'timestamp': datetime.now(),
        'hostname': u'monhost',
        'state': u'OK',
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

