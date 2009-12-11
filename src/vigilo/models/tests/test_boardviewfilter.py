# -*- coding: utf-8 -*-
"""Test suite for BoardViewFilter class"""
from vigilo.models import BoardViewFilter, Host, ServiceLowLevel, User
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestBoardViewFilter(ModelTest):
    """Test de la table BoardViewFilter"""

    klass = BoardViewFilter
    attrs = {
        'filtername': u'monfiltre',
        'username': u'manager',
        'message': u'WARNING2: SNMP error: No response from remote host',
        'trouble_ticket': u'42',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        DBSession.add(User(
            user_name=u'manager',
            fullname=u'Manager',
            email=u'foo@b.ar',
        ))

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

        service = ServiceLowLevel(
            host=host,
            servicename=u'myservice',
            command=u'halt',
            op_dep=u'+',
            priority=1,
            weight=42,
        )
        DBSession.add(service)

        DBSession.flush()
        return dict(service=service)

