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

    def test_tag_association(self):
        """Il doit être possible d'associer un tag à un hôte."""
        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
        )
        DBSession.add(host)

        service = ServiceLowLevel(
            host=host,
            servicename=u'myservice',
            op_dep=u'+',
            priority=1,
        )
        DBSession.add(service)

        self.obj.supitems.append(host)
        self.obj.supitems.append(service)
        DBSession.flush()

        host = Host.by_host_name(u'myhost')
        assert_equals(1, host.tags.count())
        assert_equals(self.obj, host.tags[0])

        service = ServiceLowLevel.by_host_service_name(
                    hostname=u'myhost', servicename=u'myservice')
        assert_equals(1, service.tags.count())
        assert_equals(self.obj, service.tags[0])

