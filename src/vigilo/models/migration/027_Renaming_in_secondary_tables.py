# -*- coding: utf-8 -*-
# Copyright (C) 2011-2013 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Effectue certains renommages dans les tables secondaires (tables de liaison) :
-   La table "submapmapnodetable" est renommée en "submaps".
-   La colonne "mapnodeid" dans cette table est renommée en "idmapnode"
    (pour la cohérence avec le reste du modèle).
-   La colonne "hostname" dans la table "host2hostclass" est remplacée
    par la colonne "idhost" afin d'améliorer les performances.

Voir ticket #800.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
from vigilo.models.tables import secondary_tables

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

    # Pour la table de liaison Host <-> HostClass
    MigrationDDL(
        [
            # Ajout de la nouvelle colonne.
            "ALTER TABLE %(fullname)s ADD COLUMN idhost INTEGER NULL",
            # Mise à jour avec les valeurs effectives.
            "UPDATE %(fullname)s SET idhost = ("
                "SELECT %(db_basename)shost.idhost "
                "FROM %(db_basename)shost "
                "WHERE %(db_basename)shost.name = %(fullname)s.hostname "
                "LIMIT 1"
            ")",
            # Ajout de la contrainte NOT NULL.
            "ALTER TABLE %(fullname)s ALTER COLUMN idhost SET NOT NULL",
            # Ajout de la contrainte référentielle.
            'ALTER TABLE %(fullname)s '
                'ADD CONSTRAINT "%(db_basename)shost2hostclass_idhost_fkey" '
                'FOREIGN KEY (idhost) '
                'REFERENCES %(db_basename)shost(idhost) '
                'ON UPDATE CASCADE ON DELETE CASCADE '
                'DEFERRABLE INITIALLY IMMEDIATE',
            # Suppression de la clé primaire actuelle
            "ALTER TABLE %(fullname)s "
                "DROP CONSTRAINT %(fullname)s_pkey",
            # Suppression de la colonne devenue obsolète.
            "ALTER TABLE %(fullname)s DROP COLUMN hostname",
            # Ajout de la nouvelle clé primaire.
            "ALTER TABLE %(fullname)s "
                "ADD PRIMARY KEY(idclass, idhost)",
        ],
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, secondary_tables.HOST_HOSTCLASS_TABLE)


    # Pour la table de liaison des sous-cartes.
    MigrationDDL(
        [
            # NB: il n'est pas nécessaire de renommer l'ancienne table
            # vers le nouveau nom : lors du vigilo-updatedb, la nouvelle
            # table est automatiquement créée avec la bonne structure.

            # Recopie des données de l'ancienne table vers la nouvelle.
            "INSERT INTO %(db_basename)ssubmaps(idmapnode, idmap) "
            "SELECT mapnodeid, idmap FROM %(db_basename)ssubmapmapnodetable",

            # Destruction de l'ancienne table.
            "DROP TABLE %(db_basename)ssubmapmapnodetable",
        ],
        context={
            'db_basename': DB_BASENAME,
            'old_table': 'submapmapnodetable',
            'new_table': 'submaps',
            'old_column': 'mapnodeid',
            'new_column': 'idmapnode',
        }
    ).execute(DBSession, secondary_tables.SUB_MAP_NODE_MAP_TABLE)
