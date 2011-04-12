# -*- coding: utf-8 -*-
"""
Vue des supitems auxquels les utilisateurs ont accès
"""

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.schema import DDL

from vigilo.models.session import DeclarativeBase, ForeignKey
from vigilo.models.configure import DB_BASENAME

from vigilo.models.tables.service import LowLevelService
from vigilo.models.tables.host import Host
from vigilo.models.tables.group import SupItemGroup
from vigilo.models.tables.grouphierarchy import GroupHierarchy
from vigilo.models.tables.datapermission import DataPermission

class UserSupItem(DeclarativeBase, object):
    """
    Table factice correspondant à une vue dans la base de données.
    Cette vue liste tous les supitems auxquels chaque utilisateur a accès.
    """

    # Doit être synchronisé avec le nom de la vue
    # (cf. DDL en fin de fichier).
    __tablename__ = 'usersupitem'

    idsupitem = Column(
        Integer,
        nullable=False,
        primary_key=True,
    )
    servicename = Column(
        Unicode(255),
        nullable=True,
        primary_key=True,
    )
    hostname = Column(
        Unicode(255),
        nullable=False,
        primary_key=True,
    )
    idsupitemgroup = Column(
        Integer,
        nullable=False,
        primary_key=True,
    )
    username = Column(
        Unicode(255),
        nullable=False,
        primary_key=True,
    )


# Suppression de la table automatiquement générée par SQLAlchemy.
DDL(
    "DROP TABLE IF EXISTS %(fullname)s"
).execute_at('after-create', UserSupItem.__table__)


# Création de la vue pour PostgreSQL.
DDL(
    r"""
    CREATE OR REPLACE VIEW %(db_basename)susersupitem AS
        SELECT %(lowlevelservice_table)s.idservice AS idsupitem,
            %(lowlevelservice_table)s.servicename AS servicename,
            %(host_table)s.name AS hostname,
            gh.idparent AS idsupitemgroup,
            %(usertousergroups_table)s.username AS username
        FROM %(lowlevelservice_table)s
        JOIN %(host_table)s
            ON %(host_table)s.idhost = %(lowlevelservice_table)s.idhost
        JOIN %(supitemgroup_table)s
            ON %(supitemgroup_table)s.idsupitem =
                %(lowlevelservice_table)s.idhost
            OR %(supitemgroup_table)s.idsupitem =
                %(lowlevelservice_table)s.idservice
        JOIN %(grouphierarchy_table)s gh
            ON gh.idchild = %(supitemgroup_table)s.idgroup
        JOIN %(grouphierarchy_table)s gh2
            ON gh2.idchild = gh.idparent
        JOIN %(datapermission_table)s
            ON %(datapermission_table)s.idgroup =
                gh2.idparent
        JOIN %(usertousergroups_table)s
            ON %(usertousergroups_table)s.idgroup =
                %(datapermission_table)s.idusergroup
    UNION ALL
        SELECT %(host_table)s.idhost AS idsupitem,
            NULL AS servicename,
            %(host_table)s.name AS hostname,
            gh.idparent AS idsupitemgroup,
            %(usertousergroups_table)s.username AS username
        FROM %(host_table)s
        JOIN %(supitemgroup_table)s
            ON %(supitemgroup_table)s.idsupitem = %(host_table)s.idhost
        JOIN %(grouphierarchy_table)s gh
            ON gh.idchild =
                %(supitemgroup_table)s.idgroup
        JOIN %(grouphierarchy_table)s gh2
            ON gh2.idchild = gh.idparent
        JOIN %(datapermission_table)s
            ON %(datapermission_table)s.idgroup =
                gh2.idparent
        JOIN %(usertousergroups_table)s
            ON %(usertousergroups_table)s.idgroup =
                %(datapermission_table)s.idusergroup;
    """,
    on='postgres',
    context={
        'db_basename': DB_BASENAME,
        'lowlevelservice_table': LowLevelService.__tablename__,
        'host_table': Host.__tablename__,
        'supitemgroup_table': '%ssupitemgroup' % DB_BASENAME,
        'usertousergroups_table': '%susertousergroups' % DB_BASENAME,
        'grouphierarchy_table': GroupHierarchy.__tablename__,
        'datapermission_table': DataPermission.__tablename__,
    },
).execute_at('after-create', UserSupItem.__table__)


# Création de la vue pour SQLite.
DDL(
    # La sous-requête est nécessaire pour contourner une limitation
    # de SQLite vis-à-vis du ORDER BY hops.
    r"""
    CREATE VIEW IF NOT EXISTS %(db_basename)susersupitem AS
        SELECT %(lowlevelservice_table)s.idservice AS idsupitem,
            %(lowlevelservice_table)s.servicename AS servicename,
            %(host_table)s.name AS hostname,
            gh.idparent AS idsupitemgroup,
            %(usertousergroups_table)s.username AS username
        FROM %(lowlevelservice_table)s
        JOIN %(host_table)s
            ON %(host_table)s.idhost = %(lowlevelservice_table)s.idhost
        JOIN %(supitemgroup_table)s
            ON %(supitemgroup_table)s.idsupitem =
                %(lowlevelservice_table)s.idhost
            OR %(supitemgroup_table)s.idsupitem =
                %(lowlevelservice_table)s.idservice
        JOIN %(grouphierarchy_table)s gh
            ON gh.idchild = %(supitemgroup_table)s.idgroup
        JOIN %(grouphierarchy_table)s gh2
            ON gh2.idchild = gh.idparent
        JOIN %(datapermission_table)s
            ON %(datapermission_table)s.idgroup =
                gh2.idparent
        JOIN %(usertousergroups_table)s
            ON %(usertousergroups_table)s.idgroup =
                %(datapermission_table)s.idusergroup
    UNION ALL
        SELECT %(host_table)s.idhost AS idsupitem,
            NULL AS servicename,
            %(host_table)s.name AS hostname,
            gh.idparent AS idsupitemgroup,
            %(usertousergroups_table)s.username AS username
        FROM %(host_table)s
        JOIN %(supitemgroup_table)s
            ON %(supitemgroup_table)s.idsupitem = %(host_table)s.idhost
        JOIN %(grouphierarchy_table)s gh
            ON gh.idchild =
                %(supitemgroup_table)s.idgroup
        JOIN %(grouphierarchy_table)s gh2
            ON gh2.idchild = gh.idparent
        JOIN %(datapermission_table)s
            ON %(datapermission_table)s.idgroup =
                gh2.idparent
        JOIN %(usertousergroups_table)s
            ON %(usertousergroups_table)s.idgroup =
                %(datapermission_table)s.idusergroup;
    """,
    on='sqlite',
    context={
        'db_basename': DB_BASENAME,
        'lowlevelservice_table': LowLevelService.__tablename__,
        'host_table': Host.__tablename__,
        'supitemgroup_table': '%ssupitemgroup' % DB_BASENAME,
        'usertousergroups_table': '%susertousergroups' % DB_BASENAME,
        'grouphierarchy_table': GroupHierarchy.__tablename__,
        'datapermission_table': DataPermission.__tablename__,
    },
).execute_at('after-create', UserSupItem.__table__)


# CREATE/DROP VIEW IF (NOT) EXISTS a été ajouté dans SQLite 3.3.8.
# group_concat() est supporté depuis SQLite 3.5.4 (+ correctif dans 3.6.14.1).
# replace() semble supporté depuis au moins SQLite 3.4.0.
# Pour plus d'information : http://www.sqlite.org/changes.html
#
# Attention : sous RHEL 5.5, c'est SQLite 3.3.6 qui est packagé
# (3.6.20 pour RHEL 6.0 -- qui peut être backporté si nécessaire).
# On suppose que SQLite 3.5.4 ou plus est disponible.
DDL(
    "DROP VIEW IF EXISTS %(db_basename)susersupitem",
    context={
        'db_basename': DB_BASENAME,
    },
).execute_at('before-drop', UserSupItem.__table__)

DDL(
    "CREATE TABLE IF NOT EXISTS %(db_basename)susersupitem (foo INTEGER)",
    context={
        'db_basename': DB_BASENAME,
    },
).execute_at('before-drop', UserSupItem.__table__)
