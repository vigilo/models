# -*- coding: utf-8 -*-
"""Test suite for HighLevelServiceDep class"""
from vigilo.models import Host, Service, HighLevelService, \
                            HighLevelServiceDepLowLevel, \
                            HighLevelServiceDepHighLevel
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_true

class TestHighLevelServiceDepLowLevel(ModelTest):
    """
    Teste les dépendances des services de haut niveau
    avec des services de bas niveau.
    """

    klass = HighLevelServiceDepLowLevel
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""
        # Le service de haut niveau pour lequel on ajoute une dépendance.
        hls = HighLevelService(
            servicename=u'virtual',
            message=u'ouch!',
            seuil_warning=60,
            seuil_critical=80,
            op_dep=u'+')
        DBSession.add(hls)
        DBSession.flush()

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
            servicename=hls.servicename,
            host_dep=host.name,
            service_dep=service.name)

    def __init__(self):
        ModelTest.__init__(self)


class TestHighLevelServiceDepHighLevel(ModelTest):
    """Teste les dépendances des services de haut niveau entre eux."""

    klass = HighLevelServiceDepHighLevel
    attrs = {}

    def do_get_dependencies(self):
        """Generate some data for the test"""
        # Le service de haut niveau pour lequel on ajoute une dépendance.
        hls1 = HighLevelService(
            servicename=u'virtual',
            message=u'ouch!',
            seuil_warning=60,
            seuil_critical=80,
            op_dep=u'+')
        DBSession.add(hls1)
        DBSession.flush()

        # La dépendance en question.
        hls2 = HighLevelService(
            servicename=u'virtual_dep',
            message=u'ouch!',
            seuil_warning=60,
            seuil_critical=80,
            op_dep=u'+')
        DBSession.add(hls2)
        DBSession.flush()

        return dict(
            servicename=hls1.servicename,
            service_dep=hls2.servicename)

    def __init__(self):
        ModelTest.__init__(self)

