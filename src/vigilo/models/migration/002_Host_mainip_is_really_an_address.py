# -*- coding: utf-8 -*-
"""
Modifie le champ "mainip" de la table Host.
Ce champ doit en fait stocker une adresse quelconque, qui ne correspond
pas nécessairement à une adresse IP (v4 ou v6). Il peut par exemple s'agir
d'un nom d'hôte complètement qualifié (FQDN).
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s RENAME COLUMN mainip TO address",
            "ALTER TABLE %(fullname)s ALTER COLUMN address TYPE varchar(255)",
        ],
    ).execute(DBSession, tables.Host.__table__)

    # Nécessite une mise à jour de VigiReport.
    actions.upgrade_vigireport = True
