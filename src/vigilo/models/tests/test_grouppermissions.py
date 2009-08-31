# -*- coding: utf-8 -*-
"""Test suite for GroupPermissions class"""
from vigilo.models import GroupPermissions, Groups
from vigilo.models.tests import ModelTest

class TestGroupPermissions(ModelTest):
    """Test de la table GroupPermissions"""

    klass = GroupPermissions
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Groups(name = "mongroup"))
        DBSession.flush()
        return dict(groupname = "mongroup")

