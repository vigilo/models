# -*- coding: utf-8 -*-
"""
Rend obligatoire la sélection la couleur et l'épaisseur du trait
dans un segment sur une carte.
"""

from sqlalchemy.schema import DDL
from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models import tables

def upgrade(migrate_engine, cluster_name):
    # Les données seront automatiquement répliquées sur le cluster
    # et donc, NE DOIVENT PAS utiliser ClusteredDDL, qui est réservé
    # aux mises à jours du schéma. On utilise donc un DDL classique.

    DDL("UPDATE %(fullname)s SET color = '#000000' WHERE color IS NULL"
        ).execute(migrate_engine, tables.MapSegment.__table__)
    DDL("UPDATE %(fullname)s SET thickness = 1 WHERE thickness IS NULL"
        ).execute(migrate_engine, tables.MapSegment.__table__)

    # On modifie le schéma des 2 attributs pour les rendre obligatoires.
    ClusteredDDL(
        [
            "ALTER TABLE %(fullname)s ALTER COLUMN color SET NOT NULL",
            "ALTER TABLE %(fullname)s ALTER COLUMN thickness SET NOT NULL",
        ],
        cluster_name=cluster_name,
        # La modification n'impacte pas la réplication
        # vers VigiReport (set n°3).
        cluster_sets=[2],
    ).execute(DBSession, tables.MapSegment.__table__)
