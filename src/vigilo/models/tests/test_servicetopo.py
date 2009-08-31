# -*- coding: utf-8 -*-
"""Test suite for ServiceTopo class"""
from vigilo.models import Service, ServiceHautNiveau, ServiceTopo
from vigilo.models.tests import 

class TestServiceTopo(ModelTest):
    """Test de la table servicetopo"""

    klass = ServiceTopo
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Service(name = "monservice"))
        DBSession.add(ServiceHautNiveau(servicename = "monservice",
            servicename_dep = "monservice"))
        DBSession.flush()
        return dict(servicename = "monservice")
