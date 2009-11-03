# -*- coding: utf-8 -*-
"""Test suite for Tag class"""
from vigilo.models import Tag, Host, ServiceLowLevel
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_equals

class TestEvents(ModelTest):
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
        hote = Host(
            name=u'monhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            )
        DBSession.add(hote)
        self.obj.hosts.append(hote)
        DBSession.flush()

        hote = Host.by_host_name(u'monhost')
        assert_equals(1, len(hote.tags))
        assert_equals(self.obj, hote.tags[0])

    def test_service_and_tag_association(self):
        """Il doit être possible d'associer un tag à un service."""
        service = ServiceLowLevel(name=u'monservice', op_dep=u'+')
        DBSession.add(service)
        self.obj.services.append(service)
        DBSession.flush()

        service = ServiceLowLevel.by_service_name(u'monservice')
        assert_equals(1, service.tags.count())
        assert_equals(self.obj, service.tags[0])

