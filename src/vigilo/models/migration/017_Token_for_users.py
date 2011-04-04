# -*- coding: utf-8 -*-
"""
Ajoute la colonne "token" dans la table User, permettant d'associer
une clé (privée) à chaque utilisateur. Cette clé pourra ensuite être
utilisée pour accéder à certaines informations de Vigilo via une API,
sans avoir recours à une authentification.
"""
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
            "ALTER TABLE %(fullname)s ADD COLUMN token VARCHAR(32) NOT NULL "
                "DEFAULT md5(cast(random() as text));",
        ]
    ).execute(DBSession, tables.User.__table__)
