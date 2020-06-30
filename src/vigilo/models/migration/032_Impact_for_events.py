# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Suppression de la table EventsAggregate.
EventsAggregate ne permet pas de représenter les événements
bruts selon la hiérarchie imposée par la topologie du réseau.
Au contraire, Impact s'appuie directement sur la topologie.

La colonne `impact` de la table CorrEvent est également
supprimée par cette migration, car elle n'était jamais
utilisée et est rendue obsolète par ce changement.

Un champ `distance` est ajouté à la table Dependency
afin de faciliter la désagrégation d'événements corrélés
suivant la topologie au niveau du corrélateur.
C'est grâce à ce champ qu'on peut se passer de EventsAggregate.

Voir également le ticket #467.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.tables import CorrEvent, Dependency

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

    # Suppression de l'ancienne colonne "impact".
    MigrationDDL(
        ["ALTER TABLE %(fullname)s DROP COLUMN impact"],
        context={}
    ).execute(DBSession, CorrEvent.__table__)

    # Ajout de la colonne "distance" dans Dependency.
    MigrationDDL(
        [
            "ALTER TABLE %(fullname)s ADD COLUMN distance INTEGER",
            "UPDATE %(fullname)s SET distance = 1 WHERE idgroup IN ("
                "SELECT idgroup FROM vigilo_dependencygroup "
                "WHERE role = 'topology'"
            ")"
        ],
    ).execute(DBSession, Dependency.__table__)

    # Invite l'utilisateur à resynchroniser sa configuration.
    # afin de mettre à jour Dependency (pour la transitivité).
    actions.sync_force = True
