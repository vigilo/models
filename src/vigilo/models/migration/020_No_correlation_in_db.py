# -*- coding: utf-8 -*-
# Copyright (C) 2006-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Les contextes de corrélation ne sont plus stockés en base de données, mais
uniquement dans memcached.
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
            "DROP TABLE vigilo_correlation_context",
        ],
    ).execute(DBSession, tables.SupItem.__table__)
