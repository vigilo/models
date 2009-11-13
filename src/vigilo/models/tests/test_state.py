# -*- coding: utf-8 -*-
"""Test suite for State class"""
from vigilo.models import State, StateName, Host, ServiceLowLevel
from vigilo.models.tests import ModelTest
from vigilo.models.session import DBSession

from nose.tools import assert_equals
from datetime import datetime

class TestState(ModelTest):
    """Test de la table State"""

    klass = State
    attrs = {
        'ip': u'127.0.0.1',
        # On ne peut pas utiliser StateName.statename_to_value ici
        # car le modèle n'est pas encore créé lorsque ce code est
        # exécuté.
        'state': 3, # = WARNING
        'statetype': u'SOFT',
        'attempt': 42,
        'timestamp': datetime.now(),
        'message': 'Foo!',
    }

    def __init__(self):
        """Initialise le test."""
        ModelTest.__init__(self)

    def do_get_dependencies(self):
        """Génère les dépendances de cette instance."""
        # Insère les noms d'états dans la base de données.
        ModelTest.do_get_dependencies(self)

        host = Host(
            name=u'monhost',
            checkhostcmd=u'halt -f',
            snmpcommunity=u'public',
            fqhn=u'localhost.localdomain',
            hosttpl=u'template',
            mainip=u'127.0.0.1',
            snmpport=u'1234',
            )
        DBSession.add(host)

        service = ServiceLowLevel(
            name=u'monservice',
            servicetype=u'foo',
            command=u'halt',
            op_dep=u'+',
        )
        DBSession.add(service)

        DBSession.flush()
        return dict(servicename=service.name, hostname=host.name)

    def test_get_by_statename(self):
        """Teste si le filtrage sur la valeur textuelle d'un état fonctionne.
        Permet de valider le comportement de state_proxy.
        """
        state = DBSession.query(State).filter(
            State.state == StateName.statename_to_value(u'WARNING')).first()
        assert_equals(self.obj, state)

