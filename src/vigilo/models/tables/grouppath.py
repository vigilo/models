# -*- coding: utf-8 -*-
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Chemins des groupes d'objets manipulés par Vigilo
(éléments supervisés, cartes, graphes).
"""

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.schema import DDL

from vigilo.models.session import DeclarativeBase, ForeignKey
from vigilo.models.tables.group import Group
from vigilo.models.tables.grouphierarchy import GroupHierarchy
from vigilo.models.configure import DB_BASENAME

class GroupPath(DeclarativeBase, object):
    """
    Table factice correspondant à une vue dans la base de données.
    Cette vue associe à chaque groupe son chemin d'accès.
    Les chemins retournés sont correctement échappés.
    """

    # Doit être synchronisé avec le nom de la vue
    # (cf. DDL en fin de fichier).
    __tablename__ = 'group_paths'

    idgroup = Column(
        'idgroup',
        Integer,
        ForeignKey(Group.idgroup),
        nullable=False,
        primary_key=True,
    )

    path = Column('path', Unicode)

    def __unicode__(self):
        return self.path

    def __repr__(self):
        return u"<%s \"%s\">" % (self.__class__.__name__, unicode(self.path))


# Suppression de la table automatiquement générée par SQLAlchemy.
DDL(
    "DROP TABLE IF EXISTS %(fullname)s"
).execute_at('after-create', GroupPath.__table__)


# Création de la vue pour PostgreSQL.
DDL(
    r"""
    CREATE OR REPLACE VIEW %(db_basename)sgroup_paths AS
    SELECT
        g2.idgroup AS idgroup,
        ('/' || array_to_string(ARRAY(
            SELECT
                replace(replace(g.name, E'\\', E'\\\\'), '/', E'\\/')
            FROM "%(group_tbl)s" g
            JOIN "%(grouphierarchy_tbl)s" gh
                ON gh.idparent = g.idgroup
            WHERE gh.idchild = g2.idgroup
            ORDER BY gh.hops DESC
        ), '/')) AS path
    FROM %(group_tbl)s g2;
    """,
    on='postgres',
    context={
        'db_basename': DB_BASENAME,
        'group_tbl': Group.__tablename__,
        'grouphierarchy_tbl': GroupHierarchy.__tablename__,
    },
).execute_at('after-create', GroupPath.__table__)


# Création de la vue pour SQLite.
DDL(
    # La sous-requête est nécessaire pour contourner une limitation
    # de SQLite vis-à-vis du ORDER BY hops.
    r"""
    CREATE VIEW IF NOT EXISTS %(db_basename)sgroup_paths AS
        SELECT
            idchild AS idgroup,
            ('/' ||
                group_concat(
                    replace(replace(name, '\', '\\'), '/', '\/'),
                    '/'
                )
            ) AS path
        FROM (
            SELECT *
            FROM "%(group_tbl)s"
            JOIN "%(grouphierarchy_tbl)s"
                ON idparent = idgroup
            ORDER BY hops DESC
        )
        GROUP BY idchild
    """,
    on='sqlite',
    context={
        'db_basename': DB_BASENAME,
        'group_tbl': Group.__tablename__,
        'grouphierarchy_tbl': GroupHierarchy.__tablename__,
    },
).execute_at('after-create', GroupPath.__table__)


# CREATE/DROP VIEW IF (NOT) EXISTS a été ajouté dans SQLite 3.3.8.
# group_concat() est supporté depuis SQLite 3.5.4 (+ correctif dans 3.6.14.1).
# replace() semble supporté depuis au moins SQLite 3.4.0.
# Pour plus d'information : http://www.sqlite.org/changes.html
#
# Attention : sous RHEL 5.5, c'est SQLite 3.3.6 qui est packagé
# (3.6.20 pour RHEL 6.0 -- qui peut être backporté si nécessaire).
# On suppose que SQLite 3.5.4 ou plus est disponible.
DDL(
    "DROP VIEW IF EXISTS %(db_basename)sgroup_paths",
    context={
        'db_basename': DB_BASENAME,
    },
).execute_at('before-drop', GroupPath.__table__)

DDL(
    "CREATE TABLE IF NOT EXISTS %(db_basename)sgroup_paths (foo INTEGER)",
    context={
        'db_basename': DB_BASENAME,
    },
).execute_at('before-drop', GroupPath.__table__)
