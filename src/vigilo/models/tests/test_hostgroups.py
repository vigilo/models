# -*- coding: utf-8 -*-
"""Test suite for HostGroups class"""
from vigilo.models import HostGroups, Host, Groups
from vigilo.models.tests import ModelTest

class TestHostGroups(ModelTest):
    """Test de la table hostgroup"""

    klass = HostGroups
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Host(name = "monhost"))
        DBSession.add(Groups(name = "mongroup"))
        DBSession.flush()
        return dict(hostname = "monhost", groupname = "mongroup")

