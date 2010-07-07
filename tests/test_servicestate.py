# -*- coding: utf-8 -*-
"""Test suite for State class"""
from datetime import datetime

from vigilo.models.tables import State, Host, LowLevelService
from vigilo.models.session import DBSession

from controller import ModelTest

class TestServiceState(ModelTest):
    """Test de la table State avec un service"""

    klass = State
    attrs = {
        # On ne peut pas utiliser StateName.statename_to_value ici
        # car le modèle n'est pas encore créé lorsque ce code est
        # exécuté.
        'state': 3, # = WARNING
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

        service = LowLevelService(
            host=host,
            servicename=u'myservice',
            command=u'halt',
            op_dep=u'+',
            weight=42,
        )
        DBSession.add(service)

        DBSession.flush()
        return dict(supitem=service)

