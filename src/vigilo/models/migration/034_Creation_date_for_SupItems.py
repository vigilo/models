# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Ajoute une colonne "creation_date" dans la table SupItem
qui contient la date de création de l'objet dans la base
de données.

La date de création des objets qui se trouvaient dans la base
de données avant l'application de cette migration est positionnée
à la date de la migration elle-même.

Voir également le ticket #999.
"""

# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

import time
import datetime

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models.tables import SupItem

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
            "ALTER TABLE %(fullname)s "
                "ADD COLUMN creation_date TIMESTAMP WITHOUT TIME ZONE",
            "UPDATE %(fullname)s SET creation_date = NOW()",
            "ALTER TABLE %(fullname)s ALTER COLUMN creation_date SET NOT NULL",
        ],
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, SupItem.__table__)
