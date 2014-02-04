# -*- coding: utf-8 -*-
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Remplit la colonne state de la table EventHistory lorsque celle-ci
est vide et que l'enregistrement correspond à un changement d'état.

Voir le ticket #1046.
"""

# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.tables import EventHistory, StateName

def upgrade(migrate_engine, actions):
    """
    Migre le modèle.

    @param migrate_engine: Connexion à la base de données,
        pouvant être utilisée durant la migration.
    @type migrate_engine: C{Engine}
    @param actions: Conteneur listant les actions à effectuer
        lorsque cette migration aura été appliquée.
    @type actions: C{MigrationActions}
    """

    MigrationDDL(
        [
            # Remplissage de la colonne state
            "UPDATE %(fullname)s "
                "SET state = s.idstatename "
                "FROM %(statename)s s "
                "WHERE ( "
                    "type_action = 'Nagios update state' "
                    "OR type_action = 'New occurrence' "
                ") "
                "AND value = s.statename "
                "AND state IS NULL",
        ],
        context={
            'statename': StateName.__tablename__,
        }
    ).execute(DBSession, EventHistory.__table__)
