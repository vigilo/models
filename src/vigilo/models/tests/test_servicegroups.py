# -*- coding: utf-8 -*-
"""Test suite for ServiceGroups class"""
from vigilo.models import Service, Groups, ServiceGroups
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestServiceGroups(ModelTest):
    """Test de la table servicegroups"""

    klass = ServiceGroups
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Service(name = u"monservice"))
        DBSession.add(Groups(name = u"mongroupe"))
        DBSession.flush()
        return dict(servicename = u"monservice", groupname = u"mongroupe")

    def __init__(self):
        ModelTest.__init__(self)

