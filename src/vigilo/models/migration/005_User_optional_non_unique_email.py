# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Supprime la contrainte d'unicité de l'adresse email
de l'utilisateur et rend le champ optionnel.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    """
    Migre le modèle.

    @param migrate_engine: Connexion à la base de données,
        pouvant être utilisée durant la migration.
    @type migrate_engine: C{Engine}
    @param actions: Conteneur listant les actions à effectuer
        lorsque cette migration aura été appliquée.
    @type actions: C{MigrationActions}
    """

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
