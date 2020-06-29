# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS GROUP – France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Remplace le champ `CorrEvent.status` par `CorrEvent.ack`.
Le changement peut améliorer les performances (utilisation d'un entier
plutôt qu'une chaîne de caractères) et évite d'avoir recours à un hack
pour permettre le tri des événements dans VigiBoard.

La liste suivante donne les correspondances entre les anciennes valeurs
(textuelles) et les nouvelles (constantes entières) :
*   "None"          : `CorrEvent.ACK_NONE`
*   "Acknowledged"  : `CorrEvent.ACK_KNOWN`
*   "AAClosed"      : `CorrEvent.ACK_CLOSED`
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.tables import CorrEvent, EventHistory

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
            "ALTER TABLE %(fullname)s "
                "ADD COLUMN ack INTEGER NOT NULL DEFAULT %(ack_none)d",
            # Migration des valeurs existantes.
            "UPDATE %(fullname)s SET ack = %(ack_none)d "
                "WHERE status = 'None'",
            "UPDATE %(fullname)s SET ack = %(ack_known)d "
                "WHERE status = 'Acknowledged'",
            "UPDATE %(fullname)s SET ack = %(ack_closed)d"
                "WHERE status = 'AAClosed'",
            # Suppression de l'ancienne colonne.
            "ALTER TABLE %(fullname)s DROP COLUMN status",
        ],
        context={
            "ack_none": CorrEvent.ACK_NONE,
            "ack_known": CorrEvent.ACK_KNOWN,
            "ack_closed": CorrEvent.ACK_CLOSED,
        }
    ).execute(DBSession, CorrEvent.__table__)

    # Corrige les entrées de l'historique des événements
    # afin que celles-ci puissent être traduites à l'affichage.
    MigrationDDL(
        [
            "UPDATE %(fullname)s SET value = 'Acknowledged and closed' "
                "WHERE value = 'AAClosed'"
        ],
        context={}
    ).execute(DBSession, EventHistory.__table__)
