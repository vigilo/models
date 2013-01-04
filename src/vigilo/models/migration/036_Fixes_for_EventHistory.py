# -*- coding: utf-8 -*-
# Copyright (C) 2006-2013 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Corrige deux problèmes concernant la table EventHistory :
-   La colonne "state" doit être renseignée avec la bonne valeur lorsque
    le champ "type_action" vaut "Forced change state".
-   Le contenu des champs "type_action" et "value" ne doit pas être
    traduit; la traduction est faite dynamiquement à l'affichage.

Il s'agit d'un complément pour les modifications déjà effectuées
lors de la migration n°35.

Voir le ticket #1046.
"""

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
            # Suppression des éventuelles traductions
            # dans la table EventHistory.
            # - "Changement de ticket" -> "Ticket change"
            "UPDATE %(fullname)s "
                "SET type_action = 'Ticket change' "
                u"WHERE type_action = 'Changement de ticket'",
            # - "Changement d'état forcé" -> "Forced change state"
            "UPDATE %(fullname)s "
                "SET type_action = 'Forced change state' "
                u"WHERE type_action = 'Changement d''état forcé'",
            # - "Changement d'état d'acquittement"
            #   -> "Acknowledgement change state"
            "UPDATE %(fullname)s "
                "SET type_action = 'Acknowledgement change state' "
                u"WHERE type_action = 'Changement d''état d''acquittement'",
            # - "Notification de changement de ticket"
            #   -> "Ticket change notification"
            "UPDATE %(fullname)s "
                "SET type_action = 'Ticket change notification' "
                u"WHERE type_action = 'Notification de changement de ticket'",
            # - "Nouvelle occurrence" -> "New occurrence"
            "UPDATE %(fullname)s "
                "SET type_action = 'New occurrence' "
                u"WHERE type_action = 'Nouvelle occurrence'",
            # - "Mise à jour d'état par Nagios" -> "Nagios update state"
            "UPDATE %(fullname)s "
                "SET type_action = 'Nagios update state' "
                u"WHERE type_action = 'Mise à jour d''état par Nagios'",

            # - "Forcé" dans le champ value lorsque type_action
            #   vaut "Acknowledgement change state"
            "UPDATE %(fullname)s "
                "SET value = 'Forced' "
                u"WHERE value = 'Forcé' "
                "AND type_action = 'Acknowledgement change state'",

            # Remplissage de la colonne state lorsque
            # type_action = "Forced change state".
            # Doit être fait APRÈS les mises à jour précédentes,
            # au cas où le texte aurait été traduit entre temps.
            "UPDATE %(fullname)s "
                "SET state = s.idstatename "
                "FROM %(statename)s s "
                "WHERE type_action = 'Forced change state' "
                "AND value = s.statename "
                "AND state IS NULL",
        ],
        context={
            'statename': StateName.__tablename__,
        }
    ).execute(DBSession, EventHistory.__table__)
