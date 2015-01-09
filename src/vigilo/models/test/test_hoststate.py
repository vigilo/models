# -*- coding: utf-8 -*-
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for State class"""
from datetime import datetime

from vigilo.models.session import DBSession
from vigilo.models.tables import State, Host

from vigilo.models.test.controller import ModelTest

class TestHostState(ModelTest):
    """Test de la table State avec un Host"""

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
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            address=u'127.0.0.1',
            snmpport=u'1234',
        )
        DBSession.add(host)

        DBSession.flush()
        return dict(idsupitem=host.idhost)

