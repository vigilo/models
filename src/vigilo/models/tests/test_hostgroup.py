# -*- coding: utf-8 -*-
"""Test suite for HostGroup class"""
from vigilo.models import HostGroup
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestHostGroups(ModelTest):
    """Test de la table hostgroup"""

    klass = HostGroup
    attrs = {
        'name': u'hostgroup',
    }

    def __init__(self):
        ModelTest.__init__(self)

