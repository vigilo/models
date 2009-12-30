# -*- coding: utf-8 -*-
"""Test suite for Downtime class"""
from vigilo.models.tests import ModelTest
from nose.tools import assert_equals
from vigilo.models.session import DBSession
from vigilo.models import Host, ServiceLowLevel, User
from vigilo.models import Downtime, DowntimeStatus

from datetime import datetime


class TestDowntimeStatus(ModelTest):
    """Unit test case for the ``DowntimeStatus`` model."""

    klass = DowntimeStatus

    attrs = dict(
        idstatus = 42,
        status = u"Foo",
    )

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def test_statename_to_value(self):
        """Teste la récupération d'une valeur de statut par son nom."""
        status_id = self.obj.status_name_to_value(u'Foo')
        assert_equals(42, status_id)

    def test_value_to_statename(self):
        """Teste la récupération d'un nom de statut en connaissant son id."""
        status_name = self.obj.value_to_status_name(42)
        assert_equals(u'Foo', status_name)
        

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
            mainip=u'127.0.0.1',
            snmpport=1234,
            weight=42,
        )
        DBSession.add(host)

        service = ServiceLowLevel(
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
            status = u"planified"
        )
        DBSession.add(status)
        DBSession.flush()
        
        return dict(supitem=service, user=user, status=status)
    
        

