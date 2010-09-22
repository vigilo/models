# -*- coding: utf-8 -*-
"""
Rend obligatoire la sélection la couleur et l'épaisseur du trait
dans un segment sur une carte.
"""

from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models import tables

def upgrade(migrate_engine):
    ClusteredDDL(
        [
            "ALTER TABLE %(fullname)s ALTER COLUMN color SET NOT NULL",
            "ALTER TABLE %(fullname)s ALTER COLUMN thickness SET NOT NULL",
        ],
        cluster_name='vigilo',
        cluster_sets=[2, 3],
    ).execute(DBSession, tables.MapSegment.__table__)
