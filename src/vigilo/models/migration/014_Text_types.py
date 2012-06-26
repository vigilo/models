# -*- coding: utf-8 -*-
# Copyright (C) 2006-2012 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Utilisation de chaînes de caractères de taille maximale fixée (VARCHAR)
au lieu de champs de texte de taille arbitraire (TEXT) lorsqu'une taille
incontrôlée n'est pas nécessaire.
Ceci permet un gain très important de performances dans les opérations
de filtrage/jointure/mise à jour.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

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
            "ALTER TABLE %(db_basename)sperfdatasource "
                "ALTER COLUMN name TYPE varchar(255)",
            "ALTER TABLE %(db_basename)sperfdatasource "
                "ALTER COLUMN \"type\" TYPE varchar(32)",
            "ALTER TABLE %(db_basename)sperfdatasource "
                "ALTER COLUMN label TYPE varchar(255)",
            "ALTER TABLE %(db_basename)seventhistory "
                "ALTER COLUMN value TYPE varchar(255)",
            "ALTER TABLE %(db_basename)shost "
                "ALTER COLUMN checkhostcmd TYPE varchar(255)",
            "ALTER TABLE %(db_basename)shost "
                "ALTER COLUMN description TYPE varchar(512)",
            "ALTER TABLE %(db_basename)slowlevelservice "
                "ALTER COLUMN command TYPE varchar(512)",
        ],
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.Host.__table__)
