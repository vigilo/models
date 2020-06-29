# -*- coding: utf-8 -*-
# Copyright (C) 2006-2020 CS GROUP – France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Ajoute une colonne "creation_date" dans la table SupItem
qui contient la date de création de l'objet dans la base
de données.

La date de création des objets qui se trouvaient dans la base de
données avant l'application de cette migration est positionnée
soit à la date du plus ancien évènement concernant l'objet s'il
en existe au moins un, soit à la date de la migration elle-même.

Voir également le ticket #999.
"""

# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.tables import SupItem

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
            "ALTER TABLE %(fullname)s "
                "ADD COLUMN creation_date TIMESTAMP WITHOUT TIME ZONE",
            "UPDATE %(fullname)s "
                "SET creation_date = sub.timestamp "
                "FROM ("
                    "SELECT "
                        "%(fullname)s.idsupitem, "
                        "COALESCE(first_events.timestamp, NOW()) AS timestamp "
                    "FROM %(fullname)s "
                    "LEFT OUTER JOIN ("
                            "SELECT "
                                "e.idsupitem, "
                                "MIN(eh.timestamp) AS timestamp "
                            "FROM vigilo_eventhistory eh "
                            "JOIN vigilo_event e "
                                "ON eh.idevent = e.idevent "
                            "GROUP BY e.idsupitem "
                        "UNION "
                            "SELECT "
                                "h.idhls AS idsupitem, "
                                "MIN(h.timestamp) as timestamp "
                            "FROM vigilo_hlshistory h "
                            "GROUP BY h.idhls"
                    ") first_events "
                        "ON %(fullname)s.idsupitem = "
                            "first_events.idsupitem"
                ") sub "
                "WHERE sub.idsupitem = %(fullname)s.idsupitem",
            "ALTER TABLE %(fullname)s ALTER COLUMN creation_date SET NOT NULL",
        ],
    ).execute(DBSession, SupItem.__table__)
