# -*- coding: utf-8 -*-
"""Test suite for ServiceDepLowOnLow class."""
from vigilo.models import Host, ServiceLowLevel, ServiceHighLevel, \
                            ServiceDepLowOnLow
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

class TestServiceDepLowOnLow(ModelTest):
    """Teste les dépendances des services de bas niveau entre eux."""

    klass = ServiceDepLowOnLow
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""
        # Le service de bas niveau pour lequel on ajoute une dépendance.
        low_dependent = ServiceLowLevel(
            name=u'low_dependent',
            op_dep=u'+',
        )
        DBSession.add(low_dependent)

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

        # Création du service physique sur lequel portera la dépendance.
        low_dependency = ServiceLowLevel(
            name=u'low_dependency',
            command=u'halt',
            op_dep=u'+',
        )
        DBSession.add(low_dependency)

        DBSession.flush()
        return dict(
            hostname=host.name,
            servicename=low_dependent.name,
            host_dep=host.name,
            service_dep=low_dependency.name)

    def __init__(self):
        ModelTest.__init__(self)

