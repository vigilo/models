# -*- coding: utf-8 -*-
"""Test suite for Downtime class"""
from datetime import datetime
from nose.tools import assert_equals

from vigilo.models.session import DBSession
from vigilo.models.tables import Host, LowLevelService, User
from vigilo.models.tables import Downtime, DowntimeStatus

from controller import ModelTest

class TestDowntime(ModelTest):
    """Unit test case for the ``Downtime`` model."""

    klass = Downtime

    attrs = dict(
        iddowntime = 42,
        entrytime = datetime.now(),
        comment = u"foo",
        start = datetime.now(),
        end = datetime.now()
    )

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Insertion de données dans la base préalable aux tests."""
        ModelTest.do_get_dependencies(self)

        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            address=u'127.0.0.1',
            snmpport=1234,
            weight=42,
        )
        DBSession.add(host)

        service = LowLevelService(
            host=host,
            servicename=u'myservice',
            command=u'halt',
            op_dep=u'+',
            weight=42,
        )
        DBSession.add(service)
        DBSession.flush()
        
        user = User(   
            user_name = u"foobar",
            email = u"foobar@example.org",
            fullname = u'Foo bar',
        )
        DBSession.add(user)
        DBSession.flush()
        
        status = DowntimeStatus(   
            status = u"Scheduled"
        )
        DBSession.add(status)
        DBSession.flush()
        
        return dict(supitem=service, user=user, status=status)
    
        

