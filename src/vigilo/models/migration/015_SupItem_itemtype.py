# -*- coding: utf-8 -*-
"""
Ajoute un index sur les noms de fichiers ConfFile, pour gagner en performances.
"""

from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, cluster_name):
    ClusteredDDL(
        [
            "ALTER TABLE %(fullname)s ADD COLUMN itemtype2 INTEGER",
            "UPDATE %(fullname)s SET itemtype2 = 1 WHERE itemtype = 'host'",
            "UPDATE %(fullname)s SET itemtype2 = 2 WHERE itemtype = 'service'",
            "UPDATE %(fullname)s SET itemtype2 = 3 WHERE itemtype = 'lowlevel'",
            "UPDATE %(fullname)s SET itemtype2 = 4 WHERE itemtype = 'highlevel'",
            "ALTER TABLE %(fullname)s ALTER COLUMN itemtype2 SET NOT NULL",
            "ALTER TABLE %(fullname)s DROP COLUMN itemtype",
            "ALTER TABLE %(fullname)s RENAME COLUMN itemtype2 TO itemtype",
 
        ],
        cluster_name=cluster_name,
        # La modification n'impacte pas la réplication
        # vers VigiReport (set n°3).
        cluster_sets=[2],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.SupItem.__table__)
