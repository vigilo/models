# -*- coding: utf-8 -*-
"""
Ajoute un champ dans la table LowLevelService
qui référence le service collector qui effectue
la collecte du service courant.
"""

from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, cluster_name):
    ClusteredDDL(
        [
            "ALTER TABLE %(fullname)s ADD COLUMN idcollector INTEGER",
            "ALTER TABLE %(fullname)s ADD CONSTRAINT %(fullname)s_idcollector_fkey "
                "FOREIGN KEY(idcollector) REFERENCES %(db_basename)ssupitem(idsupitem) "
                "ON UPDATE CASCADE ON DELETE SET NULL",
        ],
        cluster_name=cluster_name,
        cluster_sets=[2, 3],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.LowLevelService.__table__)