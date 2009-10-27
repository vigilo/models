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
        'x_pos': 1337,
        'y_pos': 42,
    }

    def __init__(self):
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Generate some data for the test"""
        DBSession.add(User(
            user_name=u'manager',
            fullname=u'Manager',
            email=u'foo@b.ar',
        ))
        DBSession.add(Host(
            name=u'monhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            ))
        DBSession.add(Graph(name=u"mongraph", template=u"", vlabel=u""))
        DBSession.flush()
        return {}

