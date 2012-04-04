# -*- coding: utf-8 -*-
# Copyright (C) 2006-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Utilise un type numérique pour représenter les différents types
d'éléments supervisés au lieu d'un champ textuel.
Ce changement permet d'obtenir de meilleures performances lors de
certaines jointures.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments

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
            "ALTER TABLE %(fullname)s ADD COLUMN itemtype2 INTEGER",
            "UPDATE %(fullname)s SET itemtype2 = 1 WHERE itemtype = 'host'",
            "UPDATE %(fullname)s SET itemtype2 = 2 WHERE itemtype = 'service'",
            "UPDATE %(fullname)s SET itemtype2 = 3 WHERE itemtype = 'lowlevel'",
            "UPDATE %(fullname)s SET itemtype2 = 4 WHERE itemtype = 'highlevel'",
            "ALTER TABLE %(fullname)s ALTER COLUMN itemtype2 SET NOT NULL",
            "ALTER TABLE %(fullname)s DROP COLUMN itemtype",
            "ALTER TABLE %(fullname)s RENAME COLUMN itemtype2 TO itemtype",

        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.SupItem.__table__)
