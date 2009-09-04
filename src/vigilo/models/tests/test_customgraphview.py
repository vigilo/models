# -*- coding: utf-8 -*-
"""Test suite for CustomGraphView class"""
from vigilo.models import CustomGraphView, Host, Graph, User
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestCustomGraphView(ModelTest):
    """Test de la table CustomGraphView"""

    klass = CustomGraphView
    attrs = {
        'viewname': u'mavue',
        'username': u'manager',
        'hostname': u'monhost',
        'graphname': u'mongraph',
        'pos_x': 1337,
        'pos_y': 42,
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        DBSession.add(User(user_name=u'manager'))
        DBSession.add(Host(name=u"monhost"))
        DBSession.add(Graph(name=u"mongraph", template=u"", vlabel=u""))
        DBSession.flush()
        return {}

