# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Ajoute une colonne dans l'historique des événements pour stocker
l'éventuel état dans lequel se retrouve l'événement.
Ceci permet d'associer des couleurs aux entrées concernant des
changements d'état.

Voir ticket #931.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.tables import EventHistory, StateName

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
            # Ajout de la nouvelle colonne.
            "ALTER TABLE %(fullname)s ADD COLUMN state INTEGER "
                "REFERENCES %(statename)s(idstatename) "
                "ON UPDATE CASCADE "
                "ON DELETE CASCADE "
                "DEFERRABLE INITIALLY IMMEDIATE",
        ],
        context={
            'statename': StateName.__tablename__,
        }
    ).execute(DBSession, EventHistory.__table__)
