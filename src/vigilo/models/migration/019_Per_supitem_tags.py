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
            # Renommage de l'ancienne table .
            "ALTER TABLE %(fullname)s RENAME TO %(db_basename)stag_migration",

            # Création de la nouvelle table à partir des anciennes.
            "CREATE TABLE %(fullname)s AS "
                "SELECT service AS idsupitem, name, value "
                "FROM %(db_basename)stag_migration "
                "NATURAL JOIN %(db_basename)stags2supitems",

            # Réaffectation de l'index à la nouvelle table
            # (précédemment affecté à *tag_migration).
            "DROP INDEX ix_%(db_basename)stag_name",
            "CREATE INDEX ix_%(db_basename)stag_name "
                "ON %(db_basename)stag (name)",

            # Ajout des contraintes sur la nouvelle table.
            "ALTER TABLE %(fullname)s ADD "
                "CONSTRAINT %(db_basename)stag_idsupitem_fkey "
                "FOREIGN KEY (idsupitem) "
                "REFERENCES %(db_basename)ssupitem(idsupitem) "
                "ON UPDATE CASCADE "
                "ON DELETE CASCADE",
            "ALTER TABLE %(fullname)s ADD PRIMARY KEY (idsupitem, name)",

            # Suppression de l'ancienne table d'association
            # et de l'ancienne table de tags.
            "DROP TABLE %(db_basename)stags2supitems",
            "DROP TABLE %(db_basename)stag_migration",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.Tag.__table__)

    # Nécessite un déploiement forcé.
    actions.deploy_force = True
