# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Refactoring des services de haut niveau pour permettre
l'utilisation de poids contextualisés.

Voir le ticket #1225.
"""

# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.tables import (
    Host,
    LowLevelService,
    HighLevelService,
    Dependency,
)

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
            # Ajout des 2 colonnes pour le poids nominal/dégradé.
            "ALTER TABLE %(fullname)s ADD COLUMN weight INTEGER "
                "DEFAULT NULL",
            "ALTER TABLE %(fullname)s ADD COLUMN warning_weight INTEGER "
                "DEFAULT NULL",

            # Migration des valeurs en place :
            # - pour les hôtes
            "UPDATE %(fullname)s "
                "SET weight = h.weight "
                "FROM %(host)s h "
                "WHERE %(fullname)s.idsupitem = h.idhost",
            # - pour les services de bas niveau
            "UPDATE %(fullname)s "
                "SET weight = lls.weight, warning_weight = lls.warning_weight "
                "FROM %(lls)s lls "
                "WHERE %(fullname)s.idsupitem = lls.idservice",
            # - pour les services de haut niveau
            "UPDATE %(fullname)s "
                "SET weight = hls.weight, warning_weight = hls.warning_weight "
                "FROM %(hls)s hls "
                "WHERE %(fullname)s.idsupitem = hls.idservice",

            # Suppression des anciennes colonnes.
            "ALTER TABLE %(host)s DROP COLUMN weight",
            "ALTER TABLE %(hls)s DROP COLUMN weight",
            "ALTER TABLE %(hls)s DROP COLUMN warning_weight",
            "ALTER TABLE %(lls)s DROP COLUMN weight",
            "ALTER TABLE %(lls)s DROP COLUMN warning_weight",
        ],
        context={
            'host': Host.__tablename__,
            'hls': HighLevelService.__tablename__,
            'lls': LowLevelService.__tablename__,
            'deps': Dependency.__tablename__,
        }
    ).execute(DBSession, Dependency.__table__)

    actions.upgrade_vigireport = True
