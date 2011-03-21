# -*- coding: utf-8 -*-
"""Test suite for the Map classe"""
from nose.tools import assert_equal
from datetime import datetime

from vigilo.models.tables import Map
from controller import ModelTest
from vigilo.models.demo.functions import add_mapgroup, add_map2group

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

    def test_by_group_and_title(self):
        g = add_mapgroup('mapgroup')
        add_map2group(self.obj, g)
        assert_equal(self.obj, Map.by_group_and_title(g, self.attrs['title']))
