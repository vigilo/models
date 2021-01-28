# -*- coding: utf-8 -*-
# Copyright (C) 2011-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Ajoute un index sur les noms de fichiers ConfFile, pour gagner en performances.
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
            "CREATE INDEX ix_vigilo_conffile_name "
            "ON vigilo_conffile (name)",
        ],
    ).execute(DBSession, tables.ConfFile.__table__)
