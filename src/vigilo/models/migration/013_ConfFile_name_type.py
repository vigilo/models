# -*- coding: utf-8 -*-
"""
Utilisation d'un champ de taille limitée au lieu d'un type TEXT
pour le nom des fichiers de configuration.
La taille du nom du fichier est fixée arbitrairement à 512 caractères
ce qui devrait suffire à la plupart des usages (le préfixe du dépôt
SVN n'est pas enregistré dans ce champ).
Cette modification permet un gain important en performances lors
d'opérations de recherche ou de jointure sur la table ConfFile.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models import tables

def upgrade(migrate_engine, actions):
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s ALTER COLUMN name TYPE varchar(512)",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.ConfFile.__table__)
