# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for Dependency class"""
from vigilo.models.tables import Dependency, Host, \
                                    LowLevelService, \
                                    DependencyGroup
from vigilo.models.session import DBSession

from controller import ModelTest

class TestDependency(ModelTest):
    """Test de la table Dependency."""

    klass = Dependency

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

        service = LowLevelService(
            host=host,
            servicename=u'myservice',
            command=u'halt',
            weight=42,
        )
        DBSession.add(service)

        depgroup = DependencyGroup(
            operator=u'+',
            role=u'topology',
            dependent=host,
        )
        DBSession.add(depgroup)
        DBSession.flush()

        return dict(
            idgroup=depgroup.idgroup,
            supitem=service,
        )
