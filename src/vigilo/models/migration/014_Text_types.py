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
            "ALTER TABLE %(db_basename)sperfdatasource "
                "ALTER COLUMN name TYPE varchar(255)",
            "ALTER TABLE %(db_basename)sperfdatasource "
                "ALTER COLUMN \"type\" TYPE varchar(32)",
            "ALTER TABLE %(db_basename)sperfdatasource "
                "ALTER COLUMN label TYPE varchar(255)",
            "ALTER TABLE %(db_basename)seventhistory "
                "ALTER COLUMN value TYPE varchar(255)",
            "ALTER TABLE %(db_basename)shost "
                "ALTER COLUMN checkhostcmd TYPE varchar(255)",
            "ALTER TABLE %(db_basename)shost "
                "ALTER COLUMN description TYPE varchar(512)",
            "ALTER TABLE %(db_basename)slowlevelservice "
                "ALTER COLUMN command TYPE varchar(512)",
        ],
        cluster_name=cluster_name,
        # La modification n'impacte pas la réplication
        # vers VigiReport (set n°3).
        cluster_sets=[2],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.Host.__table__)
