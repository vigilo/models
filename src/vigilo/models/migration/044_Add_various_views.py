# -*- coding: utf-8 -*-
# Copyright (C) 2019-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>
"""
Ajoute plusieurs vues utiles pour l'intégration
avec d'autres outils.
"""

# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL, metadata
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
    # Rien à faire de plus : les vues seront automatiquement créées
    # par SQLAlchemy lors de la re-création des objets manquants.
    pass
