# -*- coding: utf-8 -*-
"""
Ajoute un index sur les noms de fichiers ConfFile, pour gagner en performances.
"""

from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s ALTER COLUMN name TYPE varchar(512)",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.ConfFile.__table__)
