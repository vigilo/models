# -*- coding: utf-8 -*-
# Copyright (C) 2015-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Ajoute le champ "address" à la vue UserSupItem.

Voir le ticket #1734.
"""

# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL, metadata
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

    # Supprime la vue avant de la recréer avec ses nouveaux attributs.
    MigrationDDL(
        [
            "DROP VIEW %(fullname)s",
        ],
    ).execute(DBSession, tables.UserSupItem.__table__)
    metadata.create_all(bind=DBSession.bind, tables=[tables.UserSupItem.__table__])

