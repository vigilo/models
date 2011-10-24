# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for ImpactedHLS class"""
from vigilo.models.tables import HighLevelService, Host, \
                                    ImpactedHLS, ImpactedPath
from vigilo.models.session import DBSession

from controller import ModelTest

class TestImpactedHLS(ModelTest):
    """Unit test case for the ``ImpactedHLS`` model."""

    klass = ImpactedHLS
    attrs = {
        'distance': 42,
    }

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Création des dépendances du test."""
        ModelTest.do_get_dependencies(self)
        hls = HighLevelService(
            servicename=u'HLS',
            message=u'Ouch',
            warning_threshold=42,
            critical_threshold=42,
        )
        DBSession.add(hls)
        DBSession.flush()

        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            address=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()

        path = ImpactedPath(supitem=host)
        DBSession.add(path)
        DBSession.flush()

        return dict(path=path, hls=hls)
