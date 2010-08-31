# -*- coding: utf-8 -*-
"""
Supprime la contrainte d'unicité sur un nom + type de groupe.
Les groupes sont désormais organisés en arborescence et le même nom
peut donc apparaître à plusieurs endroits dans cette arborescence.
"""

from vigilo.models.session import DBSession, ClusteredDDL
from vigilo.models import tables

def upgrade(migrate_engine):
    ClusteredDDL(
        [
            "ALTER TABLE %(fullname)s DROP CONSTRAINT vigilo_group_grouptype_key",
        ],
        cluster_name='vigilo',
        cluster_sets=[2, 3],
    ).execute(DBSession, tables.Host.__table__)
