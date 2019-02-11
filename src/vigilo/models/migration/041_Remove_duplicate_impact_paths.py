# -*- coding: utf-8 -*-
# Copyright (C) 2015-2019 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Supprime de la base de données Vigilo les impactedpath en doublon.

Voir le ticket #1509.
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

    # Suppression des chemins d'impact sans HLS associé.
    MigrationDDL(
        [
            "DELETE FROM %(fullname)s WHERE idpath IN ("
                "SELECT ip.idpath FROM %(fullname)s ip LEFT OUTER JOIN "
                "%(impactedhls)s ih ON ip.idpath = ih.idpath "
                "WHERE ih.distance IS NULL"
            ")",
        ],
        context={
             'impactedhls': tables.ImpactedHLS.__tablename__,
        }
    ).execute(DBSession, tables.ImpactedPath.__table__)

    # Suppression des impactedpath en doublons.
    MigrationDDL(
        [
            "DELETE FROM %(fullname)s WHERE idpath NOT IN ("
                "SELECT DISTINCT min(ip.idpath) FROM %(fullname)s ip JOIN "
                "%(impactedhls)s ih ON ip.idpath = ih.idpath "
                "GROUP BY ip.idsupitem, ih.idhls, ih.distance);",
        ],
        context={
             'impactedhls': tables.ImpactedHLS.__tablename__,
        }
    ).execute(DBSession, tables.ImpactedPath.__table__)
