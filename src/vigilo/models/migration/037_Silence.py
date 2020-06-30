# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP - France
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
            "DROP TABLE %(table)s",
        ],
        context={
            'table': 'vigilo_downtime',
        },
    ).execute(DBSession)

    MigrationDDL(
        [
            # Suppression de la table DowntimeStatus
            "DROP TABLE %(table)s",
        ],
        context={
            'table': 'vigilo_downtime_status',
        },
    ).execute(DBSession)

