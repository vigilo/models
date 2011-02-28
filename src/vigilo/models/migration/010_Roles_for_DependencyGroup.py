# -*- coding: utf-8 -*-
"""
Ajoute un champ "role" dans la table DependencyGroup
qui indique le role des dépendances du groupe :
-   "hls" pour des dépendances logiques
-   "topology" pour des dépendances topologiques
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    MigrationDDL(
        [
            # Supprime les anciennes
            "DELETE FROM %(fullname)s",
            "ALTER TABLE %(fullname)s ADD COLUMN \"role\" VARCHAR(16) NOT NULL",
        ],
        context={}
    ).execute(DBSession, tables.DependencyGroup.__table__)

    # Nécessite un déploiement forcé.
    actions.deploy_force = True
