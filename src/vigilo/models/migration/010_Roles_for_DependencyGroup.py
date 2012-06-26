# -*- coding: utf-8 -*-
# Copyright (C) 2006-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Ajoute un champ "role" dans la table DependencyGroup
qui indique le role des dépendances du groupe :
-   "hls" pour des dépendances logiques
-   "topology" pour des dépendances topologiques
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
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
            # Supprime les anciennes
            "DELETE FROM %(fullname)s",
            "ALTER TABLE %(fullname)s ADD COLUMN \"role\" VARCHAR(16) NOT NULL",
        ],
        context={}
    ).execute(DBSession, tables.DependencyGroup.__table__)

    # Nécessite un déploiement forcé.
    actions.sync_force = True
