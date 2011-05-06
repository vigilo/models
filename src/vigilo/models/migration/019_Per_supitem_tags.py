# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Fait en sorte que les étiquettes (tags) soient associées
à un éléments supervisés et uniquement celui-ci.
De plus, les étiquettes associés à un hôte/service peuvent
désormais être manipulées comme un dictionnaire classique.
"""
from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
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
            # Préparation des données dans une table temporaire.
            "CREATE TABLE %(db_basename)stag_migration AS "
                "SELECT service AS idsupitem, name, value "
                "FROM %(db_basename)stag "
                "NATURAL JOIN %(db_basename)stags2supitems",

            # Suppression de la table d'association devenue obsolète.
            "DROP TABLE %(db_basename)stags2supitems",

            # Purge de l'ancienne table des tags.
            "TRUNCATE %(fullname)s",

            # Ajout de la nouvelle colonne.
            "ALTER TABLE %(fullname)s ADD COLUMN idsupitem INTEGER NOT NULL",

            # Mise à jour des contraintes.
            "ALTER TABLE %(fullname)s DROP CONSTRAINT %(db_basename)stag_pkey",
            "ALTER TABLE %(fullname)s ADD "
                "CONSTRAINT %(db_basename)stag_idsupitem_fkey "
                "FOREIGN KEY (idsupitem) "
                "REFERENCES %(db_basename)ssupitem(idsupitem) "
                "ON UPDATE CASCADE "
                "ON DELETE CASCADE",
            "ALTER TABLE %(fullname)s ADD PRIMARY KEY (idsupitem, name)",

            # Copie des données depuis la table temporaire,
            # puis suppression de celle-ci.
            # ATTENTION: l'ordre des champs DOIT être spécifié
            # pour coller au schéma de la table temporaire,
            # car le ADD COLUMN ajoute la colonne en fin de table.
            "INSERT INTO %(fullname)s "
                "SELECT name, value, idsupitem "
                "FROM %(db_basename)stag_migration",
            "DROP TABLE %(db_basename)stag_migration",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.Tag.__table__)

    # Nécessite un déploiement forcé.
    actions.deploy_force = True
