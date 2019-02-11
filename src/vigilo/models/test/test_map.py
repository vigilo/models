# -*- coding: utf-8 -*-
# Copyright (C) 2011-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for the Map classe"""

from datetime import datetime

from nose.tools import assert_equal

from vigilo.models.tables import Map
from vigilo.models.demo.functions import add_mapgroup, add_map2group

from vigilo.models.test.controller import ModelTest


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
        """Récupération d'une map par groupe et titre."""
        g = add_mapgroup('mapgroup')
        add_map2group(self.obj, g)
        assert_equal(self.obj, Map.by_group_and_title(g, self.attrs['title']))
