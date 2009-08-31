# -*- coding: utf-8 -*-
"""Test suite for ServiceHautNiveau class"""
from vigilo.models import Service, ServiceHautNiveau
from vigilo.models.tests import ModelTest

class TestServiceHautNiveau(ModelTest):
    """Test de la table servicehautniveau"""

    klass = ServiceHautNiveau
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""
        
        DBSession.add(Service(name = "monservice"))
        DBSession.flush()
        return dict(servicename = "monservice", servicename_dep = "monservice")

