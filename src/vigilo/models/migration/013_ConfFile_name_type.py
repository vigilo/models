# -*- coding: utf-8 -*-
# Copyright (C) 2006-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Utilisation d'un champ de taille limitée au lieu d'un type TEXT
pour le nom des fichiers de configuration.
La taille du nom du fichier est fixée arbitrairement à 512 caractères
ce qui devrait suffire à la plupart des usages (le préfixe du dépôt
SVN n'est pas enregistré dans ce champ).
Cette modification permet un gain important en performances lors
d'opérations de recherche ou de jointure sur la table ConfFile.
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
            "ALTER TABLE %(fullname)s ALTER COLUMN name TYPE varchar(512)",
        ],
    ).execute(DBSession, tables.ConfFile.__table__)
