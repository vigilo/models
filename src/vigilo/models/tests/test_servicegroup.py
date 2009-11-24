# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
from vigilo.models import ServiceLowLevel, Group, ServiceGroup, Host
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestServiceGroup(ModelTest):
    """Test de la table ServiceGroup"""

    klass = ServiceGroup
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""
        DBSession.add(Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=1234,
        ))

        service = ServiceLowLevel(
                        hostname=u'myhost',
                        servicename=u"myservice",
                        op_dep=u'+',
                        priority=1,
                    )
        DBSession.add(service)
        DBSession.add(Group(name=u"mygroup"))
        DBSession.flush()

        group = Group.by_group_name(u'mygroup')
        return dict(idservice=service.idservice, idgroup=group.idgroup)

    def __init__(self):
        ModelTest.__init__(self)

