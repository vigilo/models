# -*- coding: utf-8 -*-
"""
Utilise un type numérique pour représenter les différents types
d'éléments supervisés au lieu d'un champ textuel.
Ce changement permet d'obtenir de meilleures performances lors de
certaines jointures.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    MigrationDDL(
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
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.SupItem.__table__)
