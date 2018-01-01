# -*- coding: utf-8 -*-
# Copyright (C) 2006-2018 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
La gestion des dépendances entre les éléments supervisés
a été revue afin de permettre une plus grande souplesse.
"""

# pylint: disable-msg=W0613
# W0613: Unused arguments
# pylint: disable-msg=C0103
# Invalid name "..." (should match ...)

from vigilo.models.session import DBSession, MigrationDDL
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

    supitem_refs = [
        ('lowlevelservice', 'idservice'),
        ('highlevelservice', 'idservice'),
        ('mapservicelink', 'idref'),
        ('mapnodeservice', 'idservice'),
    ]

    hls_refs = [
        ('impactedhls', 'idhls'),
        ('hlshistory', 'idhls'),
    ]

    owner = DBSession.execute(
        'SELECT tableowner '
        'FROM pg_catalog.pg_tables '
        'WHERE schemaname = :schema '
        'AND tablename = :table;',
        params={
            'schema': "public",
            'table': tables.SupItem.__tablename__,
        }).fetchone().tableowner

    MigrationDDL(
        # Suppression des contraintes référentielles vers Service...
        [
            "ALTER TABLE vigilo_%(table)s DROP CONSTRAINT "
                "vigilo_%(table)s_%(field)s_fkey" % {
                    'table': table,
                    'field': field,
                } for (table, field) in (supitem_refs + hls_refs)
        ] +

        # ...et ajout de contraintes référentielles vers HighLevelService...
        [
            "ALTER TABLE vigilo_%(table)s ADD CONSTRAINT "
                "vigilo_%(table)s_%(field)s_fkey "
                "FOREIGN KEY(%(field)s) REFERENCES "
                "vigilo_highlevelservice(idservice) "
                "ON UPDATE CASCADE ON DELETE CASCADE" % {
                    'table': table,
                    'field': field,
                } for (table, field) in hls_refs
        ] +

        # ...ou SupItem directement selon les cas.
        [
            "ALTER TABLE vigilo_%(table)s ADD CONSTRAINT "
                "vigilo_%(table)s_%(field)s_fkey "
                "FOREIGN KEY(%(field)s) REFERENCES "
                "vigilo_supitem(idsupitem) "
                "ON UPDATE CASCADE ON DELETE CASCADE" % {
                    'table': table,
                    'field': field,
                } for (table, field) in supitem_refs
        ] +

        # Autres modifications.
        [
            # Suppression de l'ancienne table Service.
            "DROP TABLE vigilo_%(old_table)s",

            # Purge du contenu de Dependency.
            "DELETE FROM vigilo_dependency",

            # Suppression des contraintes dans Dependency.
            "ALTER TABLE %(fullname)s DROP CONSTRAINT "
                "vigilo_dependency_pkey",
            "ALTER TABLE %(fullname)s DROP CONSTRAINT "
                "vigilo_dependency_idsupitem1_fkey",
            "ALTER TABLE %(fullname)s DROP CONSTRAINT "
                "vigilo_dependency_idsupitem2_fkey",

            # Modification des champs dans Dependency.
            "ALTER TABLE %(fullname)s RENAME COLUMN idsupitem1 TO idgroup",
            "ALTER TABLE %(fullname)s RENAME COLUMN idsupitem2 TO idsupitem",

            # Ajout des nouvelles contraintes dans Dependency.
            "ALTER TABLE %(fullname)s "
                "ADD CONSTRAINT %(fullname)s_idgroup_fkey "
                "FOREIGN KEY(idgroup) "
                "REFERENCES vigilo_dependencygroup(idgroup) "
                "ON UPDATE CASCADE ON DELETE CASCADE",
            "ALTER TABLE %(fullname)s "
                "ADD CONSTRAINT %(fullname)s_idsupitem_fkey "
                "FOREIGN KEY(idsupitem) "
                "REFERENCES vigilo_supitem(idsupitem) "
                "ON UPDATE CASCADE ON DELETE CASCADE",
            "ALTER TABLE %(fullname)s ADD PRIMARY KEY (idgroup, idsupitem)",

            # Correction des droits sur DependencyGroup.
            "ALTER TABLE vigilo_dependencygroup OWNER TO %(owner)s",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'old_table': 'service',
            'owner': owner,
        }
    ).execute(DBSession, tables.Dependency.__table__)

    # Nécessite un déploiement forcé.
    actions.sync_force = True
