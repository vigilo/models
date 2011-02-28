# -*- coding: utf-8 -*-
"""
Supprime la contrainte d'unicité de l'adresse email
de l'utilisateur et rend le champ optionnel.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    MigrationDDL(
        [
            "DROP INDEX ix_%(db_basename)suser_email",
            "ALTER TABLE %(fullname)s ALTER COLUMN email DROP NOT NULL",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.User.__table__)
