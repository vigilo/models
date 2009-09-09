# -*- coding: utf-8 -*-
"""Test suite for HostGroups class"""
from vigilo.models import HostGroups, Host, Groups
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestHostGroups(ModelTest):
    """Test de la table hostgroup"""

    klass = HostGroups
    attrs = {}

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(
            name=u'monhost',
            checkhostcmd=u'halt -f',
            community=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            port=u'1234',
            ))
        DBSession.add(Groups(name = u"mongroup"))
        DBSession.flush()
        return dict(hostname = u"monhost", groupname = u"mongroup")

