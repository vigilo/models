# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Ajoute une colonne "warning_weight" dans les tables LowLevelService
et HighLevelService (services de bas/haut niveau, respectivement).

Ce nouveau champ permet de définir un poids différent pour le service,
selon que son état est OK ou WARNING.

Voir également le ticket #918.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.tables import LowLevelService, HighLevelService

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

    for table in (HighLevelService, LowLevelService):
        MigrationDDL(
            [
                "ALTER TABLE %(fullname)s ADD COLUMN warning_weight INTEGER",
                # Par défaut le poids dans l'état WARNING
                # est le même que dans l'état OK.
                "UPDATE %(fullname)s SET warning_weight = weight",
                "ALTER TABLE %(fullname)s ALTER COLUMN warning_weight SET NOT NULL",
            ],
        ).execute(DBSession, table.__table__)

    # Pas besoin de forcer un vigiconf deploy.
    # Si l'utilisateur veut utiliser des poids différents,
    # il devra de toutes façons modifier les fichiers de
    # configuration XML et refaire un deploy.
