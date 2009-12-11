# -*- coding: utf-8 -*-
"""Test suite for HostClass class"""
from vigilo.models import Host, HostClass
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestHostClass(ModelTest):
    """Test de la table HostClass"""

    klass = HostClass
    attrs = {
        'name': u'MyHostClass',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        host =  Host(
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
        return dict(hosts=[host])

