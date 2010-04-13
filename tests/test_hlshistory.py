# -*- coding: utf-8 -*-
"""Test suite for HLSHistory class"""
from datetime import datetime

from vigilo.models.tables import HighLevelService, HLSHistory, StateName
from vigilo.models.session import DBSession

from controller import ModelTest

class TestHLSHistory(ModelTest):
    """Unit test case for the ``HLSHistory`` model."""

    klass = HLSHistory
    attrs = {
        'timestamp': datetime.now(),
    }

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Création des dépendances du test."""
        super(TestHLSHistory, self).do_get_dependencies()

        hls = HighLevelService(
            servicename=u'HLS',
            op_dep=u'+',
            message=u'Ouch',
            warning_threshold=42,
            critical_threshold=42,
            priority=42,
        )
        DBSession.add(hls)
        DBSession.flush()

        idstatename = StateName.statename_to_value(u'WARNING')

        return dict(hls=hls, idstatename=idstatename)

