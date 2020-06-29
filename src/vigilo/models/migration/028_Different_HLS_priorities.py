# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS GROUP – France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Permet d'associer des priorités différentes aux événements
qui impactent un service de haut niveau en fonction de l'état
dans lequel celui-ci se retrouve (UNKNOWN, WARNING ou CRITICAL).

Voir ticket #874.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.tables import HighLevelService

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

    # vigilo-updatedb crée automatiquement la nouvelle table de liaison
    # chargée de stocker les priorités.
    # Donc, les tâches restantes sont uniquement :
    # - Suppression de l'ancienne colonne "priority" sur les HLS.
    # - Invitation pour que l'administrateur relance VigiConf.

    MigrationDDL(
        [
            # Ajout de la nouvelle colonne.
            "ALTER TABLE %(fullname)s DROP COLUMN priority",
        ],
        context={}
    ).execute(DBSession, HighLevelService.__table__)

    # Invite l'utilisateur à resynchroniser sa configuration.
    actions.sync_force = True
