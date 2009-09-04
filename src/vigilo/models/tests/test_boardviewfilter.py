# -*- coding: utf-8 -*-
"""Test suite for BoardViewFilter class"""
from vigilo.models import BoardViewFilter, Host, Service
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestBoardViewFilter(ModelTest):
    """Test de la table BoardViewFilter"""

    klass = BoardViewFilter
    attrs = {
        'username': u'manager',
        'hostname': u'monhost',
        'servicename': u'monservice',
        'output': u'WARNING2: SNMP error: No response from remote host',
        'trouble_ticket': u'42',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        DBSession.add(Host(name = u"monhost"))
        DBSession.add(Service(name = u"monservice"))
        DBSession.flush()
        return {}

