# -*- coding: utf-8 -*-
"""Test suite for ServiceGroup class"""
from vigilo.models import ServiceGroup, GraphGroup, MapGroup, HostGroup
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestServiceGroup(ModelTest):
    """Test de la table ServiceGroup"""

    klass = ServiceGroup
    attrs = {
        'name': u'servicegroup'
    }

    def __init__(self):
        ModelTest.__init__(self)
        
        
class TestMapGroup(ModelTest):
    """Test de la table MapGroup"""

    klass = MapGroup
    attrs = {
        'name': u'mapgroup'
    }

    def __init__(self):
        ModelTest.__init__(self)
        

class TestHostGroups(ModelTest):
    """Test de la table hostgroup"""

    klass = HostGroup
    attrs = {
        'name': u'hostgroup',
    }

    def __init__(self):
        ModelTest.__init__(self)
        
class TestGraphGroup(ModelTest):
    """Test de la table GraphGroup"""

    klass = GraphGroup
    attrs = dict(name = u"mongraph")

    def __init__(self):
        ModelTest.__init__(self)

