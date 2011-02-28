# -*- coding: utf-8 -*-
"""
Ajoute la possibilité de désactiver un serveur Vigilo.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s ADD COLUMN disabled BOOLEAN "
                "NOT NULL DEFAULT false",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.VigiloServer.__table__)
