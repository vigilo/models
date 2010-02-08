# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
Contient les tables intermédiaires utilisées dans les relations de type
"plusieurs-à-plusieurs" sans attributs propres.
Les tables définies ci-dessous ne correspondent qu'à des relations binaires.
Si vous devez représenter une relation ternaire (ou plus), créez une
table spécifique dans le reste du modèle (ie. : une classe qui hérite
de DeclarativeBase).
"""

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Unicode, Integer
from vigilo.models.configure import db_basename, metadata

USERGROUP_PERMISSION_TABLE = Table(
    db_basename + 'usergrouppermissions', metadata,
    Column('idgroup', Integer, ForeignKey(
                db_basename + 'usergroup.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                db_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
)

SUPITEM_TAG_TABLE = Table(
    db_basename + 'tags2supitems', metadata,
    Column('service', Integer, ForeignKey(
                db_basename + 'supitem.idsupitem',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('name', Unicode(255), ForeignKey(
                db_basename + 'tag.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

EVENTSAGGREGATE_TABLE = Table(
    db_basename + 'eventsaggregate', metadata,
    Column('idevent', Integer, ForeignKey(
                db_basename + 'event.idevent',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idcorrevent', Integer, ForeignKey(
                db_basename + 'correvent.idcorrevent',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
)

GROUP_PERMISSION_TABLE = Table(
    db_basename + 'grouppermissions', metadata,
    Column('idgroup', Integer, ForeignKey(
                db_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idpermission', Integer, ForeignKey(
                db_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

USER_GROUP_TABLE = Table(
    db_basename + 'usertousergroups', metadata,
    Column('username', Unicode(255), ForeignKey(
                db_basename + 'user.user_name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idgroup', Integer, ForeignKey(
                db_basename + 'usergroup.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

MAP_PERMISSION_TABLE = Table(
    db_basename + 'mappermissions', metadata,
    Column('idmap', Integer, ForeignKey(
                db_basename + 'map.idmap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                db_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

MAP_GROUP_TABLE = Table(
    db_basename + 'mapgroup', metadata,
    Column('idgroup', Integer, ForeignKey(
                db_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idmap', Integer, ForeignKey(
                db_basename + 'map.idmap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)                           
)

SUB_MAP_NODE_MAP_TABLE = Table(
    db_basename + 'submapmapnodetable', metadata,
    Column('mapnodeid', Integer, ForeignKey(
                db_basename + 'mapnode.idmapnode',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idmap', Integer, ForeignKey(
                db_basename + 'map.idmap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)                           
)

HOST_HOSTCLASS_TABLE = Table(
    db_basename + 'host2hostclass', metadata,
    Column('hostname', Unicode(255), ForeignKey(
                db_basename + 'host.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idclass', Integer, ForeignKey(
                db_basename + 'hostclass.idclass',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

HOST_GROUP_TABLE = Table(
    db_basename + 'hostgroup', metadata,
    Column('idhost', Integer, ForeignKey(
                db_basename + 'host.idhost',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgroup', Integer, ForeignKey(
                db_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

SERVICE_GROUP_TABLE = Table(
    db_basename + 'servicegroup', metadata,
    Column('idservice', Integer, ForeignKey(
                db_basename + 'service.idservice',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgroup', Integer, ForeignKey(
                db_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

GRAPH_GROUP_TABLE = Table(
    db_basename + 'graphgroup', metadata,
    Column('idgraph', Integer, ForeignKey(
                db_basename + 'graph.idgraph',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgroup', Integer, ForeignKey(
                db_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

GRAPH_PERFDATASOURCE_TABLE = Table(
    db_basename + 'graphperfdatasource', metadata,
    Column('idperfdatasource', Integer, ForeignKey(
                db_basename + 'perfdatasource.idperfdatasource',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgraph', Integer, ForeignKey(
                db_basename + 'graph.idgraph',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

