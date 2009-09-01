# -*- coding: utf-8 -*-
"""Test suite for HostGroups class"""
from vigilo.models import HostGroups, Host, Groups
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestHostGroups(ModelTest):
    """Test de la table hostgroup"""

    klass = HostGroups
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(name = u"monhost"))
        DBSession.add(Groups(name = u"mongroup"))
        DBSession.flush()
        return dict(hostname = u"monhost", groupname = u"mongroup")

