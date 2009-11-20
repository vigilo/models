# -*- coding: utf-8 -*-
"""Test suite for HostServiceData class"""
from vigilo.models import HostServiceData, Host, ServiceLowLevel
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestHostServiceData(ModelTest):
    """
    Teste l'affectation de données à un couple (L{Host}, L{ServiceLowLevel}).

    Par exemple, on teste l'affectation d'un "poids" au couple.
    Plus le poids de ce couple est élevé, plus il est critique
    pour l'infrastructure supervisée.
    L'unité utilisée pour représenter le poids est choisie par
    l'organisme qui effectue la supervision.
    Il peut être déterminé par des SLA, etc.
    """

    klass = HostServiceData
    attrs = {
        'weight': 100,
        'priority': 1,
    }

    def do_get_dependencies(self):
        """Generate some data for the test"""
        # Création de l'hôte physique sur lequel portera la dépendance.
        host = Host(
            name=u'physical',
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'foo',
            mainip=u'127.0.0.1',
            snmpport=42,
        )
        DBSession.add(host)
        DBSession.flush()

        # Création du service physique sur lequel portera la dépendance.
        service = ServiceLowLevel(
            name=u'physical',
            command=u'halt',
            op_dep=u'+',
        )
        DBSession.add(service)
        DBSession.flush()

        return dict(
            hostname=host.name,
            servicename=service.name)

    def __init__(self):
        ModelTest.__init__(self)

