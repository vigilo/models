# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Version initiale du modèle.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

def upgrade(migrate_engine, actions):
    """
    @param migration_engine: Connexion pouvant être utilisée pour exécuter
        directement du DDL. Il n'est généralement pas nécessaire d'y avoir
        recours. Privilégiez L{vigilo.models.session.MigrationDDL} à la
        place.
    @type actions: C{Engine}
    @param actions: Objet indiquant les actions supplémentaires qui devront
        être menées suite à la migration du schéma.
    @type actions: C{MigrationActions}
    """
    pass
