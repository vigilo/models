# -*- coding: utf-8 -*-
"""
Ajoute différents indexes qui permettent d'accroitre de manière
importante les performances du corrélateur.

Les indexes ajoutés concernent :
- La colonne "idsupitem" de la table "CorrEvent".
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models.tables import Event

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
            "CREATE INDEX ix_%(db_basename)sevent_idsupitem "
                "ON %(db_basename)sevent (idsupitem)",
        ],
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, Event.__table__)

