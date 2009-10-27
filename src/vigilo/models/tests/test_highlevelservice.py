# -*- coding: utf-8 -*-
"""Test suite for HighLevelService class"""
from vigilo.models import Service, State, Host, HostServiceData, \
                            HighLevelService, HighLevelServiceDepLowLevel, \
                            HighLevelServiceDepHighLevel
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession
from nose.tools import assert_true
from datetime import datetime

def create_hls_dependancies():
    # Création de l'hôte physique.
    host = Host(
        name=u'physical',
        checkhostcmd=u'halt',
        snmpcommunity=u'public',
        fqhn=u'localhost',
        hosttpl=u'foo',
        mainip=u'127.0.0.1',
        snmpport=42)
    DBSession.add(host)
    DBSession.flush()

    # Création de services physiques.
    service_tpl = {
        'servicetype': u'foo',
        'command': u'halt',
    }
    service1 = Service(name=u'service1', **service_tpl)
    service2 = Service(name=u'service2', **service_tpl)
    service3 = Service(name=u'service3', **service_tpl)

    DBSession.add(service1)
    DBSession.add(service2)
    DBSession.add(service3)
    DBSession.flush()

    # Affectation de données aux couples (hôte, service).
    weight1 = HostServiceData(
        hostname=u'physical',
        servicename=u'service1',
        weight=1,
        priority=1,
    )
    weight2 = HostServiceData(
        hostname=u'physical',
        servicename=u'service2',
        weight=2,
        priority=1,
    )
    weight3 = HostServiceData(
        hostname=u'physical',
        servicename=u'service3',
        weight=3,
        priority=1,
    )

    DBSession.add(weight1)
    DBSession.add(weight2)
    DBSession.add(weight3)
    DBSession.flush()

    # Création des dépendances sur les services techniques.
    dep_tpl = {
        'servicename': u'virtual',
        'host_dep': u'physical',
    }

    dep1 = HighLevelServiceDepLowLevel(service_dep=service1.name, **dep_tpl)
    dep2 = HighLevelServiceDepLowLevel(service_dep=service2.name, **dep_tpl)
    dep3 = HighLevelServiceDepLowLevel(service_dep=service3.name, **dep_tpl)

    DBSession.add(dep1)
    DBSession.add(dep2)
    DBSession.add(dep3)
    DBSession.flush()

def change_state(servicename, servicestate):
    # Change l'état d'un des services techniques (de bas niveau).
    state = State(hostname=u'physical', servicename=servicename,
        statename=servicestate, attempt=42, timestamp=datetime.now())
    DBSession.add(state)
    DBSession.flush()


class TestHighLevelServiceEvenHigherServices(ModelTest):
    """
    Teste la récupération des services de niveau n+1 pour un
    L{HighLevelService} de niveau n.
    """

    klass = HighLevelService
    attrs = {
        'servicename': u'low',
        'message': u'ouch!',
        'warning_threshold': 60,
        'critical_threshold': 80,
        'op_dep': u'+',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def test_higher_services_retrieval(self):
        """
        Vérifie que l'on peut récupérer les services de haut niveau
        qui dépendent d'un service de haut donné.
        """

        # Création d'un service de haut niveau qui dépend du nôtre.
        higher = HighLevelService(**self.attrs)
        higher.servicename = u'high'
        DBSession.add(higher)
        DBSession.flush()

        # Ajout de la dépendance.
        dep = HighLevelServiceDepHighLevel(
            servicename=higher.servicename,
            service_dep=self.obj.servicename)
        DBSession.add(dep)
        DBSession.flush()

        higher_services = self.obj.higher_services
        assert_true(len(higher_services) == 1,
            "Expected 1 higher level service, got %d" % len(higher_services))
        assert_true(higher_services[0] == higher,
            "Unexpected higher service")


class TestHighLevelServicePlus(ModelTest):
    """Teste un service de haut niveau de type '+'."""

    klass = HighLevelService
    attrs = {
        'servicename': u'virtual',
        'message': u'ouch!',
        'warning_threshold': 60,
        'critical_threshold': 80,
        'op_dep': u'+',
    }

    def __init__(self):
        ModelTest.__init__(self)

    def test_weight_computation(self):
        create_hls_dependancies()

        # On effectue le teste une première fois dans l'état nominal.
        weight = self.obj.weight
        assert_true(weight == 6,
            msg='Expected weight = 6, but received %d' % weight)

        # Puis on fait varier l'état des dépendances.
        change_state(servicename=u'service3', servicestate=u'WARNING')

        weight = self.obj.weight
        assert_true(weight == 3,
            msg='Expected weight = 3, but received %d' % weight)


class TestHighLevelServiceOr(TestHighLevelServicePlus):
    """Teste un service de haut niveau de type 'ou'."""

    attrs = {
        'servicename': u'virtual',
        'message': u'ouch!',
        'warning_threshold': 60,
        'critical_threshold': 80,
        'op_dep': u'ou',
    }

    def test_weight_computation(self):
        create_hls_dependancies()

        # On effectue le teste une première fois dans l'état nominal.
        weight = self.obj.weight
        assert_true(weight == 3,
            msg='Expected weight = 3, but received %d' % weight)

        # Puis on fait varier l'état des dépendances.
        change_state(servicename=u'service3', servicestate=u'WARNING')

        weight = self.obj.weight
        assert_true(weight == 2,
            msg='Expected weight = 2, but received %d' % weight)


class TestHighLevelServiceAnd(TestHighLevelServicePlus):
    """Teste un service de haut niveau de type 'et'."""

    attrs = {
        'servicename': u'virtual',
        'message': u'ouch!',
        'warning_threshold': 60,
        'critical_threshold': 80,
        'op_dep': u'et',
    }

    def test_weight_computation(self):
        create_hls_dependancies()

        # On effectue le teste une première fois dans l'état nominal.
        weight = self.obj.weight
        assert_true(weight == 1,
            msg='Expected weight = 1, but received %d' % weight)

        # Puis on fait varier l'état des dépendances.
        change_state(servicename=u'service3', servicestate=u'WARNING')

        weight = self.obj.weight
        assert_true(weight == 0,
            msg='Expected weight = 0, but received %d' % weight)

