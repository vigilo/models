# -*- coding: utf-8 -*-
"""
Utilisation de chaînes de caractères de taille maximale fixée (VARCHAR)
au lieu de champs de texte de taille arbitraire (TEXT) lorsqu'une taille
incontrôlée n'est pas nécessaire.
Ceci permet un gain très important de performances dans les opérations
de filtrage/jointure/mise à jour.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    MigrationDDL(
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
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.Host.__table__)
