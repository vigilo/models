# -*- coding: utf-8 -*-
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Supprime les tables Downtime et DowntimeStatus, et les remplace
par les tables Silence et SilenceState.

Ceci fait suite à la reprise des travaux sur la mise en silence (voir le ticket
#1187).
"""

# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME

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
            # Suppression de la table Downtime
            "DROP TABLE %(db_basename)s%(table)s",
        ],
        context={
            'db_basename': DB_BASENAME,
            'table': 'downtime',
        },
    ).execute(DBSession)

    MigrationDDL(
        [
            # Suppression de la table DowntimeStatus
            "DROP TABLE %(db_basename)s%(table)s",
        ],
        context={
            'db_basename': DB_BASENAME,
            'table': 'downtime_status',
        },
    ).execute(DBSession)

