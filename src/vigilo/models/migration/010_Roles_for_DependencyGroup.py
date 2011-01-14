# -*- coding: utf-8 -*-
"""
Ajoute un champ "role" dans la table DependencyGroup
qui indique le role des dépendances du groupe :
-   "hls" pour des dépendances logiques
-   "topology" pour des dépendances topologiques
"""

from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, cluster_name):
    ClusteredDDL(
        [
            # Supprime les anciennes
            "DELETE FROM %(fullname)s",
            "ALTER TABLE %(fullname)s ADD COLUMN \"role\" VARCHAR(16) NOT NULL",
        ],
        cluster_name=cluster_name,
        cluster_sets=[2],
        context={}
    ).execute(DBSession, tables.DependencyGroup.__table__)

    print   "ATTENTION: Though the schema migration completed successfully,\n" \
            "you should re-deploy your configuration using option --force " \
            "to finish the migration."
