# -*- coding: utf-8 -*-
"""
Ajoute la possibilité de désactiver un serveur Vigilo.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments

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
            "ALTER TABLE %(fullname)s ADD COLUMN disabled BOOLEAN "
                "NOT NULL DEFAULT false",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.VigiloServer.__table__)
