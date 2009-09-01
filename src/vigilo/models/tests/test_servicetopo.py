# -*- coding: utf-8 -*-
"""Test suite for ServiceTopo class"""
from vigilo.models import Service, ServiceHautNiveau, ServiceTopo
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestServiceTopo(ModelTest):
    """Test de la table servicetopo"""

    klass = ServiceTopo
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        DBSession.add(Service(name = u"monservice"))
        DBSession.add(ServiceHautNiveau(servicename = u"monservice",
            servicename_dep = u"monservice"))
        DBSession.flush()
        return dict(servicename = u"monservice")

