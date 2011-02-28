# -*- coding: utf-8 -*-
"""
Rend obligatoire la sélection la couleur et l'épaisseur du trait
dans un segment sur une carte.
"""

from sqlalchemy.schema import DDL
from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    # Mise à jour des valeurs avec les valeurs par défaut.
    DDL("UPDATE %(fullname)s SET color = '#000000' WHERE color IS NULL"
        ).execute(migrate_engine, tables.MapSegment.__table__)
    DDL("UPDATE %(fullname)s SET thickness = 1 WHERE thickness IS NULL"
        ).execute(migrate_engine, tables.MapSegment.__table__)

    # On modifie le schéma des 2 attributs pour les rendre obligatoires.
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s ALTER COLUMN color SET NOT NULL",
            "ALTER TABLE %(fullname)s ALTER COLUMN thickness SET NOT NULL",
        ],
    ).execute(DBSession, tables.MapSegment.__table__)
