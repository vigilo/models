# -*- coding: utf-8 -*-
"""
Modifie le champ "mainip" de la table Host.
Ce champ doit en fait stocker une adresse quelconque, qui ne correspond
pas nécessairement à une adresse IP (v4 ou v6). Il peut par exemple s'agir
d'un nom d'hôte complètement qualifié (FQDN).
"""

from sqlalchemy.schema import DDL
from vigilo.models import tables

def upgrade(migrate_engine):
    DDL('ALTER TABLE %(fullname)s RENAME COLUMN mainip TO address'
        ).execute(migrate_engine, tables.Host.__table__)
    DDL('ALTER TABLE %(fullname)s ALTER COLUMN address TYPE varchar(255)'
        ).execute(migrate_engine, tables.Host.__table__)

def downgrade(migrate_engine):
    DDL('ALTER TABLE %(fullname)s ALTER COLUMN address TYPE varchar(40)'
        ).execute(migrate_engine, tables.Host.__table__)
    DDL('ALTER TABLE %(fullname)s RENAME COLUMN address TO mainip'
        ).execute(migrate_engine, tables.Host.__table__)

