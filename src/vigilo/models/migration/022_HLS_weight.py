# -*- coding: utf-8 -*-
"""
Rend le poids associé aux services de haut niveau statique.

Ce changement permet de simplifier grandement la configuration
des services de haut niveau dans VigiConf puisqu'il n'est plus
nécessaire de calculer (récursivement) l'apport relatif de chaque
dépendance pour choisir les seuils à appliquer au service de haut
niveau.

Voir le ticket #406.
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