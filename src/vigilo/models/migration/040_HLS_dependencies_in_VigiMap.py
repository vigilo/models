# -*- coding: utf-8 -*-
# Copyright (C) 2015-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Permet l'affichage de l'état des dépendances d'un service de haut niveau
dans VigiMap (#1280).
"""

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

    # Création du type (pour postgresql).
    MigrationDDL(
        [
            "DROP TYPE IF EXISTS vigilo_mapnodehls_show_deps RESTRICT",
            "CREATE TYPE vigilo_mapnodehls_show_deps "
                "AS ENUM ('never','problems','always')",
        ],
    ).execute(DBSession, tables.MapNodeService.__table__)

    # Ajout de la colonne.
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s "
                "ADD COLUMN show_deps vigilo_mapnodehls_show_deps NULL",
        ],
    ).execute(DBSession, tables.MapNodeService.__table__)

    # Mise à jour de la table avec la valeur par défaut.
    MigrationDDL(
        [
            "UPDATE %(fullname)s SET show_deps = 'never'",
        ],
    ).execute(DBSession, tables.MapNodeService.__table__)

    # Ajout des contraintes.
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s ALTER COLUMN show_deps SET NOT NULL",
        ],
    ).execute(DBSession, tables.MapNodeService.__table__)

