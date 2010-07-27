# -*- coding: utf-8 -*-
"""
Supprime la contrainte d'unicité sur un nom + type de groupe.
Les groupes sont désormais organisés en arborescence et le même nom
peut donc apparaître à plusieurs endroits dans cette arborescence.
"""

from sqlalchemy.schema import DDL
from vigilo.models import tables

def upgrade(migrate_engine):
    DDL('ALTER TABLE %(fullname)s DROP CONSTRAINT vigilo_group_grouptype_key'
        ).execute(migrate_engine, tables.group.Group.__table__)

def downgrade(migrate_engine):
    DDL('ALTER TABLE %(fullname)s DROP CONSTRAINT vigilo_group_grouptype_key'
        ).execute(migrate_engine, tables.group.Group.__table__)


