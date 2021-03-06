# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for HostClass class"""
from vigilo.models.session import DBSession
from vigilo.models.tables import Host, HostClass

from vigilo.models.test.controller import ModelTest

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
        ModelTest.do_get_dependencies(self)
        host =  Host(
            name=u'myhost',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            address=u'127.0.0.1',
            snmpport=1234,
        )
        DBSession.add(host)
        return dict(hosts=[host])

