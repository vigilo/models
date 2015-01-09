# -*- coding: utf-8 -*-
# Copyright (C) 2011-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for DependencyGroup class"""
from vigilo.models.tables import DependencyGroup, Host
from vigilo.models.session import DBSession

from vigilo.models.test.controller import ModelTest

class TestDependencyGroup(ModelTest):
    """Test de la table DependencyGroup."""

    klass = DependencyGroup

    attrs = {
        'operator': u'+',
        'role': u'topology',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
        host = Host(
            name=u'myhost',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            address=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)

        return dict(dependent=host)
