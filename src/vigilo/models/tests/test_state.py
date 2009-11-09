# -*- coding: utf-8 -*-
"""Test suite for State class"""
from vigilo.models import State, Host, ServiceLowLevel
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

from nose.tools import assert_equals
from datetime import datetime

class TestState(ModelTest):
    """Test de la table State"""

    klass = State
    attrs = {
        'ip': u'127.0.0.1',
        'statename': u'WARNING',
        'statetype': u'SOFT',
        'attempt': 42,
        'timestamp': datetime.now(),
        'message': 'Foo!',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        host = Host(
            name=u'monhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            )
        DBSession.add(host)

        service = ServiceLowLevel(
            name=u'monservice',
            servicetype=u'foo',
            command=u'halt',
            op_dep=u'+',
        )
        DBSession.add(service)

        DBSession.flush()
        return dict(servicename=service.name, hostname=host.name)

    def test_get_by_statename(self):
        state = DBSession.query(State).filter(
            State.statename == u'WARNING').first()
        assert_equals(self.obj, state)

