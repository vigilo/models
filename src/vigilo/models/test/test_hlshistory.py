# -*- coding: utf-8 -*-
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for HLSHistory class"""
from datetime import datetime

from vigilo.models.tables import HLSHistory, StateName
from vigilo.models.demo import functions

from vigilo.models.test.controller import ModelTest

class TestHLSHistory(ModelTest):
    """Unit test case for the ``HLSHistory`` model."""

    klass = HLSHistory
    attrs = {
        'timestamp': datetime.now(),
    }

    def do_get_dependencies(self):
        """Création des dépendances du test."""
        super(TestHLSHistory, self).do_get_dependencies()
        hls = functions.add_highlevelservice(u'HLS')
        idstatename = StateName.statename_to_value(u'WARNING')
        return dict(hls=hls, idstatename=idstatename)
