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
            "CREATE INDEX ix_%(db_basename)scorrevent_timestamp_active "
            "ON %(db_basename)scorrevent (timestamp_active)",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.CorrEvent.__table__)
