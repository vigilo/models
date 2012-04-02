# -*- coding: utf-8 -*-
"""Test suite for VigiloServer class"""
from nose.tools import assert_equals

from vigilo.models.tables import VigiloServer

from vigilo.models.test.controller import ModelTest

class TestVigiloServer(ModelTest):


    klass = VigiloServer
    attrs = {
        'name': u'supserver.example.com',
    }
    
    def __init__(self):
        ModelTest.__init__(self)
    
    def test_by_vigiloserver_name(self):
        """Récupération d'un serveur Vigilo par son nom."""
        ob = VigiloServer.by_vigiloserver_name(u'supserver.example.com')
        assert_equals(self.obj, ob)

