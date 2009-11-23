# -*- coding: utf-8 -*-
"""Test suite for Tag class"""
from vigilo.models import Tag, Host, ServiceLowLevel
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_equals

class TestTag(ModelTest):
    """Test de la table Tag"""

    klass = Tag
    attrs = {
        'name': u'test',
        'value': u'Foo bar baz',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def test_host_and_tag_association(self):
        """Il doit être possible d'associer un tag à un hôte."""
        host = Host(
            hostname=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
        )
        DBSession.add(host)
        self.obj.hosts.append(host)
        DBSession.flush()

        host = Host.by_host_name(u'myhost')
        assert_equals(1, len(host.tags))
        assert_equals(self.obj, host.tags[0])

    def test_service_and_tag_association(self):
        """Il doit être possible d'associer un tag à un service."""
        host = Host(
            hostname=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
        )
        DBSession.add(host)

        service = ServiceLowLevel(
            hostname=u'myhost',
            servicename=u'myservice',
            op_dep=u'+',
            priority=1,
        )
        DBSession.add(service)
        self.obj.services.append(service)
        DBSession.flush()

        service = ServiceLowLevel.by_host_service_name(
                    hostname=u'myhost', servicename=u'myservice')
        assert_equals(1, service.tags.count())
        assert_equals(self.obj, service.tags[0])

