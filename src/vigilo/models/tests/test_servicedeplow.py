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
        # Création de l'hôte physique qui contiendra les services techniques.
        host = Host(
            name=u'physical',
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'foo',
            mainip=u'127.0.0.1',
            snmpport=42,
        )
        DBSession.add(host)

        # Le service de bas niveau pour lequel on ajoute une dépendance.
        low_dependent = ServiceLowLevel(
            host=host,
            servicename=u'low_dependent',
            command=u'halt',
            op_dep=u'+',
            priority=1,
        )
        DBSession.add(low_dependent)

        # Création du service physique sur lequel portera la dépendance.
        low_dependency = ServiceLowLevel(
            host=host,
            servicename=u'low_dependency',
            command=u'halt',
            op_dep=u'+',
            priority=1,
        )
        DBSession.add(low_dependency)

        DBSession.flush()
        return dict(
            service=low_dependent,
            service_dep=low_dependency,
        )

    def __init__(self):
        ModelTest.__init__(self)

