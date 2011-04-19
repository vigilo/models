# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
La gestion des dépendances entre les éléments supervisés
a été revue afin de permettre une plus grande souplesse.
"""

from vigilo.models.session import DBSession, MigrationDDL
from vigilo.models.configure import DB_BASENAME
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
            "ALTER TABLE %%(db_basename)s%(table)s DROP CONSTRAINT "
                "%%(db_basename)s%(table)s_%(field)s_fkey" % {
                    'table': table,
                    'field': field,
                } for (table, field) in (supitem_refs + hls_refs)
        ] +

        # ...et ajout de contraintes référentielles vers HighLevelService...
        [
            "ALTER TABLE %%(db_basename)s%(table)s ADD CONSTRAINT "
                "%%(db_basename)s%(table)s_%(field)s_fkey "
                "FOREIGN KEY(%(field)s) REFERENCES "
                "%%(db_basename)shighlevelservice(idservice) "
                "ON UPDATE CASCADE ON DELETE CASCADE" % {
                    'table': table,
                    'field': field,
                } for (table, field) in hls_refs
        ] +

        # ...ou SupItem directement selon les cas.
        [
            "ALTER TABLE %%(db_basename)s%(table)s ADD CONSTRAINT "
                "%%(db_basename)s%(table)s_%(field)s_fkey "
                "FOREIGN KEY(%(field)s) REFERENCES "
                "%%(db_basename)ssupitem(idsupitem) "
                "ON UPDATE CASCADE ON DELETE CASCADE" % {
                    'table': table,
                    'field': field,
                } for (table, field) in supitem_refs
        ] +

        # Autres modifications.
        [
            # Suppression de l'ancienne table Service.
            "DROP TABLE %(db_basename)s%(old_table)s",

            # Purge du contenu de Dependency.
            "DELETE FROM %(db_basename)sdependency",

            # Suppression des contraintes dans Dependency.
            "ALTER TABLE %(fullname)s DROP CONSTRAINT "
                "%(db_basename)sdependency_pkey",
            "ALTER TABLE %(fullname)s DROP CONSTRAINT "
                "%(db_basename)sdependency_idsupitem1_fkey",
            "ALTER TABLE %(fullname)s DROP CONSTRAINT "
                "%(db_basename)sdependency_idsupitem2_fkey",

            # Modification des champs dans Dependency.
            "ALTER TABLE %(fullname)s RENAME COLUMN idsupitem1 TO idgroup",
            "ALTER TABLE %(fullname)s RENAME COLUMN idsupitem2 TO idsupitem",

            # Ajout des nouvelles contraintes dans Dependency.
            "ALTER TABLE %(fullname)s "
                "ADD CONSTRAINT %(fullname)s_idgroup_fkey "
                "FOREIGN KEY(idgroup) "
                "REFERENCES %(db_basename)sdependencygroup(idgroup) "
                "ON UPDATE CASCADE ON DELETE CASCADE",
            "ALTER TABLE %(fullname)s "
                "ADD CONSTRAINT %(fullname)s_idsupitem_fkey "
                "FOREIGN KEY(idsupitem) "
                "REFERENCES %(db_basename)ssupitem(idsupitem) "
                "ON UPDATE CASCADE ON DELETE CASCADE",
            "ALTER TABLE %(fullname)s ADD PRIMARY KEY (idgroup, idsupitem)",

            # Correction des droits sur DependencyGroup.
            "ALTER TABLE %(db_basename)sdependencygroup OWNER TO %(owner)s",
        ],
        # Le nom de la contrainte dépend du préfixe utilisé.
        context={
            'db_basename': DB_BASENAME,
            'old_table': 'service',
            'owner': owner,
        }
    ).execute(DBSession, tables.Dependency.__table__)

    # Nécessite un déploiement forcé.
    actions.deploy_force = True
