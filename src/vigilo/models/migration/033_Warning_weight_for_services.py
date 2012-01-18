# -*- coding: utf-8 -*-
"""
Ajoute une colonne "warning_weight" dans les tables LowLevelService
et HighLevelService (services de bas/haut niveau, respectivement).

Ce nouveau champ permet de définir un poids différent pour le service,
selon que son état est OK ou WARNING.

Voir également le ticket #918.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
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
            context={
                'db_basename': DB_BASENAME,
            }
        ).execute(DBSession, table.__table__)

    # Pas besoin de forcer un vigiconf deploy.
    # Si l'utilisateur veut utiliser des poids différents,
    # il devra de toutes façons modifier les fichiers de
    # configuration XML et refaire un deploy.
