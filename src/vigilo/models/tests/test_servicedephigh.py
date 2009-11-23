# -*- coding: utf-8 -*-
"""Test suite for ServiceDepHighOnLow & ServiceDepHighOnHigh classes."""
from vigilo.models import Host, ServiceLowLevel, ServiceHighLevel, \
                            ServiceDepHighOnHigh, ServiceDepHighOnLow
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

#class TestServiceDepHighOnHigh(ModelTest):
#    """Teste les dépendances des services de haut niveau entre eux."""

#    klass = ServiceDepHighOnHigh
#    attrs = {}

#    def do_get_dependencies(self):
#        """Generate some data for the test"""
#        # Le service de haut niveau pour lequel on ajoute une dépendance.
#        hls1 = ServiceHighLevel(
#            name=u'virtual',
#            message=u'ouch!',
#            warning_threshold=60,
#            critical_threshold=80,
#            op_dep=u'+',
#        )
#        DBSession.add(hls1)

#        # Le service de haut niveau sur lequel porte la dépendance.
#        hls2 = ServiceHighLevel(
#            name=u'virtual_dep',
#            message=u'ouch!',
#            warning_threshold=60,
#            critical_threshold=80,
#            op_dep=u'+',
#        )
#        DBSession.add(hls2)

#        DBSession.flush()
#        return dict(
#            servicename=hls1.name,
#            service_dep=hls2.name)

#    def __init__(self):
#        ModelTest.__init__(self)


class TestServiceDepHighOnLow(ModelTest):
    """
    Teste les dépendances des services de haut niveau
    sur des services de bas niveau.
    """

    klass = ServiceDepHighOnLow
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""

        # Le service de haut niveau pour lequel on ajoute une dépendance.
        hls = ServiceHighLevel(
            servicename=u'virtual',
            message=u'ouch!',
            warning_threshold=60,
            critical_threshold=80,
            op_dep=u'+'
        )
        DBSession.add(hls)

        # Création de l'hôte physique sur lequel portera la dépendance.
        host = Host(
            hostname=u'physical',
            checkhostcmd=u'halt',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'foo',
            mainip=u'127.0.0.1',
            snmpport=42,
        )
        DBSession.add(host)

        # Création du service physique sur lequel portera la dépendance.
        service = ServiceLowLevel(
            hostname=u'physical',
            servicename=u'physical',
            command=u'halt',
            op_dep=u'+',
            priority=1,
        )
        DBSession.add(service)

        DBSession.flush()

        return dict(servicename=hls.servicename, service_dep=service)

    def __init__(self):
        ModelTest.__init__(self)

