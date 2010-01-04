# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
Contient les tables intermédiaires utilisées dans les relations de type
"plusieurs-à-plusieurs".
"""

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.types import Unicode, Integer
from .vigilo_bdd_config import bdd_basename, metadata

USERGROUP_PERMISSION_TABLE = Table(
    bdd_basename + 'usergrouppermissions', metadata,
    Column('idgroup', Integer, ForeignKey(
                bdd_basename + 'usergroup.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                bdd_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
)

SUPITEM_TAG_TABLE = Table(
    bdd_basename + 'tags2supitems', metadata,
    Column('service', Integer, ForeignKey(
                bdd_basename + 'supitem.idsupitem',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('name', Unicode(255), ForeignKey(
                bdd_basename + 'tag.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

EVENTSAGGREGATE_TABLE = Table(
    bdd_basename + 'eventsaggregate', metadata,
    Column('idevent', Integer, ForeignKey(
                bdd_basename + 'event.idevent',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idcorrevent', Integer, ForeignKey(
                bdd_basename + 'correvent.idcorrevent',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
)

GROUP_PERMISSION_TABLE = Table(
    bdd_basename + 'grouppermissions', metadata,
    Column('idgroup', Integer, ForeignKey(
                bdd_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idpermission', Integer, ForeignKey(
                bdd_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

USER_GROUP_TABLE = Table(
    bdd_basename + 'usertousergroups', metadata,
    Column('username', Unicode(255), ForeignKey(
                bdd_basename + 'user.user_name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idgroup', Integer, ForeignKey(
                bdd_basename + 'usergroup.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

MAP_PERMISSION_TABLE = Table(
    bdd_basename + 'mappermissions', metadata,
    Column('idmap', Integer, ForeignKey(
                bdd_basename + 'map.idmap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                bdd_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

MAP_GROUP_TABLE = Table(
    bdd_basename + 'mapgroup', metadata,
    Column('idgroup', Integer, ForeignKey(
                bdd_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idmap', Integer, ForeignKey(
                bdd_basename + 'map.idmap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)                           
)

SUB_MAP_NODE_MAP_TABLE = Table(
    bdd_basename + 'submapmapnodetable', metadata,
    Column('mapnodeid', Integer, ForeignKey(
                bdd_basename + 'mapnode.idmapnode',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idmap', Integer, ForeignKey(
                bdd_basename + 'map.idmap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)                           
)

HOST_HOSTCLASS_TABLE = Table(
    bdd_basename + 'host2hostclass', metadata,
    Column('hostname', Unicode(255), ForeignKey(
                bdd_basename + 'host.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idclass', Integer, ForeignKey(
                bdd_basename + 'hostclass.idclass',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

HOST_GROUP_TABLE = Table(
    bdd_basename + 'hostgroup', metadata,
    Column('idhost', Integer, ForeignKey(
                bdd_basename + 'host.idhost',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgroup', Integer, ForeignKey(
                bdd_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

SERVICE_GROUP_TABLE = Table(
    bdd_basename + 'servicegroup', metadata,
    Column('idservice', Integer, ForeignKey(
                bdd_basename + 'service.idservice',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgroup', Integer, ForeignKey(
                bdd_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

GRAPH_GROUP_TABLE = Table(
    bdd_basename + 'graphgroup', metadata,
    Column('idgraph', Integer, ForeignKey(
                bdd_basename + 'graph.idgraph',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgroup', Integer, ForeignKey(
                bdd_basename + 'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

GRAPH_PERFDATASOURCE_TABLE = Table(
    bdd_basename + 'graphperfdatasource', metadata,
    Column('idperfdatasource', Integer, ForeignKey(
                bdd_basename + 'perfdatasource.idperfdatasource',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgraph', Integer, ForeignKey(
                bdd_basename + 'graph.idgraph',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

