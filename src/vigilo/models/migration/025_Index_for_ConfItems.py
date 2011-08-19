# -*- coding: utf-8 -*-
"""
Ajoute un index et une contrainte d'unicité sur les colonnes
"name" et "idsupitem" de la table ConfItem.
Cet ajout améliore les performances des "deploy" de VigiConf.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models.tables import ConfItem

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
            "ALTER TABLE %(fullname)s "
            "ADD CONSTRAINT ix_%(fullname)s_key UNIQUE (name, idsupitem)",
        ],
    ).execute(DBSession, ConfItem.__table__)

