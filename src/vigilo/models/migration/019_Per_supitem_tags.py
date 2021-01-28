# -*- coding: utf-8 -*-
# Copyright (C) 2006-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Fait en sorte que les étiquettes (tags) soient associées
à un éléments supervisés et uniquement celui-ci.
De plus, les étiquettes associés à un hôte/service peuvent
désormais être manipulées comme un dictionnaire classique.
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
            # Préparation des données dans une table temporaire.
            "CREATE TABLE vigilo_tag_migration AS "
                "SELECT service AS idsupitem, name, value "
                "FROM vigilo_tag "
                "NATURAL JOIN vigilo_tags2supitems",

            # Suppression de la table d'association devenue obsolète.
            "DROP TABLE vigilo_tags2supitems",

            # Purge de l'ancienne table des tags.
            "TRUNCATE %(fullname)s",

            # Ajout de la nouvelle colonne.
            "ALTER TABLE %(fullname)s ADD COLUMN idsupitem INTEGER NOT NULL",

            # Mise à jour des contraintes.
            "ALTER TABLE %(fullname)s DROP CONSTRAINT vigilo_tag_pkey",
            "ALTER TABLE %(fullname)s ADD "
                "CONSTRAINT vigilo_tag_idsupitem_fkey "
                "FOREIGN KEY (idsupitem) "
                "REFERENCES vigilo_supitem(idsupitem) "
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
                "FROM vigilo_tag_migration",
            "DROP TABLE vigilo_tag_migration",
        ],
    ).execute(DBSession, tables.Tag.__table__)

    # Nécessite un déploiement forcé.
    actions.sync_force = True
