# -*- coding: utf-8 -*-
# Copyright (C) 2006-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Modifie le champ "mainip" de la table Host.
Ce champ doit en fait stocker une adresse quelconque, qui ne correspond
pas nécessairement à une adresse IP (v4 ou v6). Il peut par exemple s'agir
d'un nom d'hôte complètement qualifié (FQDN).
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments

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
            "ALTER TABLE %(fullname)s RENAME COLUMN mainip TO address",
            "ALTER TABLE %(fullname)s ALTER COLUMN address TYPE varchar(255)",
        ],
    ).execute(DBSession, tables.Host.__table__)

    # Nécessite une mise à jour de VigiReport.
    actions.upgrade_vigireport = True
