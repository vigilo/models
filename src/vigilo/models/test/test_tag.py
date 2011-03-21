# -*- coding: utf-8 -*-
"""Test suite for Tag class"""
from nose.tools import assert_equals

from vigilo.models.tables import Tag, Host, LowLevelService
from vigilo.models.session import DBSession

from controller import ModelTest

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
            address=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)

        service = LowLevelService(
            host=host,
            servicename=u'myservice',
            weight=42,
        )
        DBSession.add(service)

        self.obj.supitems.append(host)
        self.obj.supitems.append(service)
        DBSession.flush()

        host = Host.by_host_name(u'myhost')
        assert_equals(1, len(host.tags))
        assert_equals(self.obj, host.tags[0])

        service = LowLevelService.by_host_service_name(
                    hostname=u'myhost', servicename=u'myservice')
        assert_equals(1, len(service.tags))
        assert_equals(self.obj, service.tags[0])