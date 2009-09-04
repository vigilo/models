# -*- coding: utf-8 -*-
"""Test suite for ServiceHautNiveau class"""
from vigilo.models import Service, ServiceHautNiveau
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestServiceHautNiveau(ModelTest):
    """Test de la table servicehautniveau"""

    klass = ServiceHautNiveau
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""
        
        DBSession.add(Service(name = u"monservice"))
        DBSession.flush()
        return dict(servicename = u"monservice", servicename_dep = u"monservice")

    def __init__(self):
        ModelTest.__init__(self)

