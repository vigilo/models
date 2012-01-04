# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for State class"""
from datetime import datetime

from nose.tools import assert_equals

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
            snmpcommunity=u'public',
            description=u'My Host',
            hosttpl=u'template',
            address=u'127.0.0.1',
            snmpport=u'1234',
            weight=42,
        )
        DBSession.add(host)
        DBSession.flush()

        service = LowLevelService(
            host=host,
            servicename=u'myservice',
            command=u'halt',
            weight=42,
        )
        DBSession.add(service)

        DBSession.flush()
        return dict(idsupitem=service.idservice)

    def test_query_obj(self):
        """Vérifie les données insérées."""
        # On est obligé de redéfinir cette fonction parce que plusieurs états
        # ont été insérés lorsqu'on a ajouté l'hôte et le service.
        obj = DBSession.query(State).join(
                    (LowLevelService, LowLevelService.idservice == State.idsupitem)
                ).filter(
                    LowLevelService.servicename == u"myservice"
                ).one()
        for key, value in self.attrs.iteritems():
            assert_equals(getattr(obj, key), value)
