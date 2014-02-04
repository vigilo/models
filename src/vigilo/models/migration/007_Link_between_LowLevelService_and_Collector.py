# -*- coding: utf-8 -*-
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Ajoute un champ dans la table LowLevelService
qui référence le service collector qui effectue
la collecte du service courant.
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
            "ALTER TABLE %(fullname)s ADD COLUMN idcollector INTEGER",
            "ALTER TABLE %(fullname)s "
                "ADD CONSTRAINT %(fullname)s_idcollector_fkey "
                "FOREIGN KEY(idcollector) "
                "REFERENCES %(db_basename)ssupitem(idsupitem) "
                "ON UPDATE CASCADE ON DELETE SET NULL",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
        }
    ).execute(DBSession, tables.LowLevelService.__table__)

    # Nécessite une mise à jour de VigiReport.
    actions.upgrade_vigireport = True
