# -*- coding: utf-8 -*-
# Copyright (C) 2006-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Test suite for State class"""
from datetime import datetime

from nose.tools import assert_equals

from vigilo.models.tables import State, LowLevelService
from vigilo.models.demo import functions
from vigilo.models.session import DBSession

from vigilo.models.test.controller import ModelTest

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

    def do_get_dependencies(self):
        """Génère les dépendances de cette instance."""
        # Insère les noms d'états dans la base de données.
        ModelTest.do_get_dependencies(self)
        host = functions.add_host(u'myhost')
        service = functions.add_lowlevelservice(host, u'myservice')
        return dict(idsupitem=service.idservice)

    def test_query_obj(self):
        """Vérifie les données insérées."""
        # On est obligé de redéfinir cette fonction parce que plusieurs états
        # ont été insérés lorsqu'on a ajouté l'hôte et le service.
        obj = DBSession.query(
                State
            ).join(
                (LowLevelService, LowLevelService.idservice == State.idsupitem),
            ).filter(LowLevelService.servicename == u"myservice").one()
        for key, value in self.attrs.iteritems():
            assert_equals(getattr(obj, key), value)
