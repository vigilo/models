# -*- coding: utf-8 -*-
"""
Ajoute un index sur la colonne timestamp_active des correvents, pour optimiser
une requête utilisée dans la règle UpdateOccurencesCount du corrélateur.
Ticket: #774
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

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
            "UPDATE %(fullname)s SET weight = 1 WHERE weight IS NULL",
            "ALTER TABLE %(fullname)s ALTER COLUMN weight SET NOT NULL",
        ],
    ).execute(DBSession, tables.HighLevelService.__table__)

    # Nécessite un déploiement forcé.
    actions.sync_force = True
