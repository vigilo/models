# -*- coding: utf-8 -*-
"""Test suite for ServiceWeight class"""
from vigilo.models import ServiceWeight, Host, Service
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_true

class TestServiceWeight(ModelTest):
    """
    Teste l'affectation de "poids" à un couple (L{Host}, L{Service}).

    Plus le poids de ce couple est élevé, plus il est critique
    pour l'infrastructure supervisée.
    L'unité du poids est choisie par l'organisme qui effectue la supervision.
    Il peut être déterminé par des SLA, etc.
    """

    klass = ServiceWeight
    attrs = {
        'weight': 100,
    }

    def do_get_dependencies(self):
        """Generate some data for the test"""
        # Création de l'hôte physique sur lequel portera la dépendance.
        host = Host(
            name=u'physical',
            checkhostcmd=u'halt',
            community=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'foo',
            mainip=u'127.0.0.1',
            port=42,
            )
        DBSession.add(host)
        DBSession.flush()

        # Création du service physique sur lequel portera la dépendance.
        service = Service(
            name=u'physical',
            servicetype=u'foo',
            command=u'halt',
            )
        DBSession.add(service)
        DBSession.flush()

        return dict(
            hostname=host.name,
            servicename=service.name)

    def __init__(self):
        ModelTest.__init__(self)

