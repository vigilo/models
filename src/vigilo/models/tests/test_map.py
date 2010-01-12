# -*- coding: utf-8 -*-
"""Test suite for ServiceLowLevel & ServiceHighLevel classes"""
from vigilo.models import Map
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from datetime import datetime

class TestMap(ModelTest):
    """Test de la classe Map."""

    klass = Map
    attrs = {
        'mtime' : datetime.today(),
        'title' : u'Carte 1',
        'background_color' : u'#00CC99',
        'background_image' : u'France',
        'background_position' : u'top right',
        'background_repeat' : u'no-repeat', 
    }

    def __init__(self):
        ModelTest.__init__(self)

