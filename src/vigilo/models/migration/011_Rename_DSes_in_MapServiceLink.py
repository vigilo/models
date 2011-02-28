# -*- coding: utf-8 -*-
"""
Renomme les attributs correspondant aux indicateurs de métrologie
sur les liens dans les cartes (MapServiceLink) de la manière suivante :
- "idds_from_to_to" devient "idds_out"
- "idds_to_to_from" devient "idds_in"
- "ds_from_to_to" devient "ds_out"
- "ds_to_to_from" devient "ds_in"
Ces changements permettent de rendre le backend cohérent avec
la nomenclature utilisée dans le frontend.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    MigrationDDL(
        [
            # Renommage des attributs.
            # Les attributs en "ds_*" sont des relations basées sur "idds_*"
            # et seront donc automatiquement mis à jour.
            "ALTER TABLE %(fullname)s RENAME COLUMN idds_from_to_to TO idds_out",
            "ALTER TABLE %(fullname)s RENAME COLUMN idds_to_to_from TO idds_in",
        ],
        context={}
    ).execute(DBSession, tables.MapServiceLink.__table__)
