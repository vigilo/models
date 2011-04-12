# -*- coding: utf-8 -*-
"""
Ajout d'une vue associant à chaque utilisateur
les objets supervisés auxquels il a accès.
"""

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

    # En elle-même, cette migration ne change pas le modèle,
    # car la vue est créée automatiquement par create_all()
    # dans le websetup.
    #
    # Cependant, le fait d'avoir un script de migration permet
    # d'associer un numéro de version à l'ajout de la vue,
    # et donc de faciliter le suivi des évolutions.
    pass
