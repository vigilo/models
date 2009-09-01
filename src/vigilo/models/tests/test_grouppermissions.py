# -*- coding: utf-8 -*-
"""Test suite for GroupPermissions class"""
from vigilo.models import GroupPermissions, Groups, Permission
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestGroupPermissions(ModelTest):
    """Test de la table GroupPermissions"""

    klass = GroupPermissions
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Groups(name = u"mongroup"))
        DBSession.add(Permission(idpermission = 1,
            permission_name = u"mapermission"))
        DBSession.flush()
        return dict(groupname = u"mongroup", idpermission = 1)

