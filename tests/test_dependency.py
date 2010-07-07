# -*- coding: utf-8 -*-
"""Test suite for Dependency class"""
from vigilo.models.tables import Dependency, Host, LowLevelService
from vigilo.models.session import DBSession

from controller import ModelTest

class TestDependency(ModelTest):
    """Test de la table Dependency."""

    klass = Dependency

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
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
            command=u'halt',
            op_dep=u'+',
            weight=42,
        )
        DBSession.add(service)

        DBSession.flush()
        return dict(supitem1=host, supitem2=service)

