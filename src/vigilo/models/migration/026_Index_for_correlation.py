# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Ajoute différents indexes qui permettent d'accroitre de manière
importante les performances du corrélateur.

Les indexes ajoutés concernent :
- La colonne "idsupitem" de la table "Event".
- La colonne "current_state" de la table "Event".
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models.tables import Event

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
            "CREATE INDEX ix_%(db_basename)sevent_idsupitem "
                "ON %(db_basename)sevent (idsupitem)",
            "CREATE INDEX ix_%(db_basename)sevent_current_state "
                "ON %(db_basename)sevent (current_state)",
        ],
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, Event.__table__)
