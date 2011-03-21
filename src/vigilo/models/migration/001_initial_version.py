# -*- coding: utf-8 -*-
"""
Version initiale du modèle.
"""

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
