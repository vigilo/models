# -*- coding: utf-8 -*-
# Copyright (C) 2015-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Permet de masquer les étiquettes des objets sur les cartes.

Voir le ticket #1609.
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

    # Remplace l'attribut "minimize" des nœuds des cartes par un attribut
    # "hide_label" (pour mieux refléter ce que fait l'attribut).
    # Ajoute également un attribut "hide_tags" pour permettre de masquer
    # les étiquettes des nœuds.
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s RENAME COLUMN minimize TO hide_label",
            "ALTER TABLE %(fullname)s ADD COLUMN hide_tags boolean "
                "NOT NULL DEFAULT TRUE",
            "ALTER TABLE %(fullname)s ALTER COLUMN hide_tags DROP DEFAULT",
        ],
    ).execute(DBSession, tables.MapNode.__table__)

