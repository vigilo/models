# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Modifie la taille du champ qui stocke le condensat des mots de passe
afin de permettre le stockage de condensats de plus grande taille.

Nécessaire pour gérer les évolutions dans le temps des algorithmes
de hachage (cf. #156).
"""

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
            # Mise à jour du champ "password" de la table "user"
            # pour accepter des condensats salés/avec des options
            # et/ou des algorithmes ayant des sorties plus longues.
            "ALTER TABLE %(fullname)s ALTER COLUMN password TYPE varchar(256)",
        ],
    ).execute(DBSession, tables.User.__table__)

