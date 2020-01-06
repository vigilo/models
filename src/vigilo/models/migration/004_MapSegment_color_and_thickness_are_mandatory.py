# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Rend obligatoire la sélection la couleur et l'épaisseur du trait
dans un segment sur une carte.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from sqlalchemy.schema import DDL
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

    # Mise à jour des valeurs avec les valeurs par défaut.
    DDL(
        "UPDATE %(fullname)s SET color = '#000000' WHERE color IS NULL",
        obj=tables.MapSegment.__table__,
        bind=migrate_engine,
    )
    DDL(
        "UPDATE %(fullname)s SET thickness = 1 WHERE thickness IS NULL",
        obj=tables.MapSegment.__table__,
        bind=migrate_engine,
    )

    # On modifie le schéma des 2 attributs pour les rendre obligatoires.
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s ALTER COLUMN color SET NOT NULL",
            "ALTER TABLE %(fullname)s ALTER COLUMN thickness SET NOT NULL",
        ],
    ).execute(DBSession, tables.MapSegment.__table__)
