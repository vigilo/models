# -*- coding: utf-8 -*-
"""Test suite for HostGroup class"""
from vigilo.models import HostGroup, Host, Group
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestHostGroups(ModelTest):
    """Test de la table hostgroup"""

    klass = HostGroup
    attrs = {}

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        DBSession.add(Host(
            hostname=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=1234,
            ))
        DBSession.add(Group(name=u"group"))
        DBSession.flush()

        group = Group.by_group_name(u'group')
        return dict(hostname=u"host", idgroup=group.idgroup)

