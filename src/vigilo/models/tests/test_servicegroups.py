# -*- coding: utf-8 -*-
"""Test suite for ServiceGroups class"""
from vigilo.models import Service, Groups, ServiceGroups
from vigilo.models.tests import ModelTest

class TestServiceGroups(ModelTest):
    """Test de la table servicegroups"""

    klass = ServiceGroups
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Service(name = "monservice"))
        DBSession.add(Groups(name = "mongroupe"))
        DBSession.flush()
        return dict(servicename = "monservice", groupname = "mongroupe")

