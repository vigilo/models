# -*- coding: utf-8 -*-
"""Test suite for PerfDataSource class"""
from vigilo.models.tables import Host, LowLevelService, PerfDataSource
from vigilo.models.session import DBSession

from controller import ModelTest

class TestPerfDataSource(ModelTest):
    """Test de la table perfdatasource"""

    klass = PerfDataSource
    attrs = {
        'name': u'myperfsource',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        ModelTest.do_get_dependencies(self)
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
        DBSession.flush()
        return dict(host=host)

