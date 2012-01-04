# -*- coding: utf-8 -*-
"""
Supprime l'attribut "checkhostcmd" de la table Host.
Cet attribut n'a jamais été utilisé et ne le sera probablement
jamais car l'utilisation de la base de données dans les
générateurs de VigiConf (ce pour quoi cet attribut existait)
serait trop coûteuse.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.tables import Host

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
            "ALTER TABLE %(fullname)s DROP COLUMN checkhostcmd",
        ],
        context={
        }
    ).execute(DBSession, Host.__table__)
