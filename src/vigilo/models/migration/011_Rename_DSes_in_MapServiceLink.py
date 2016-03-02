# -*- coding: utf-8 -*-
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

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

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

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
