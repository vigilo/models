# -*- coding: utf-8 -*-
"""Test suite for VigiloServer class"""
from vigilo.models import VigiloServer
from vigilo.models.session import DBSession

from controller import ModelTest

class TestVigiloServer(ModelTest):


    klass = VigiloServer
    attrs = {
        'name': u'supserver.example.com',
        'description': u'a vigilo supervision server',
    }
    
    def __init__(self):
        ModelTest.__init__(self)

