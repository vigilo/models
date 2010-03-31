# -*- coding: utf-8 -*-
"""Test suite for ImpactedPath class"""
from vigilo.models.tables import ImpactedPath, Host
from vigilo.models.session import DBSession

from controller import ModelTest

class TestImpactedPath(ModelTest):
    """Unit test case for the ``ImpactedPath`` model."""

    klass = ImpactedPath
    attrs = {}

    def __init__(self):
        """Initialisation du test."""
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Création des dépendances du test."""
        host = Host(
            name=u'myhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()

        return dict(supitem=host)

