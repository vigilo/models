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

from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from vigilo.models.configure import metadata, ForeignKey, Table

USERGROUP_PERMISSION_TABLE = Table(
    'usergrouppermissions', metadata,
    Column('idgroup', Integer, ForeignKey(
                'usergroup.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
)

SUPITEM_TAG_TABLE = Table(
    'tags2supitems', metadata,
    Column('service', Integer, ForeignKey(
                'supitem.idsupitem',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('name', Unicode(255), ForeignKey(
                'tag.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

EVENTSAGGREGATE_TABLE = Table(
    'eventsaggregate', metadata,
    Column('idevent', Integer, ForeignKey(
                'event.idevent',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idcorrevent', Integer, ForeignKey(
                'correvent.idcorrevent',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
)

GROUP_PERMISSION_TABLE = Table(
    'grouppermissions', metadata,
    Column('idgroup', Integer, ForeignKey(
                'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idpermission', Integer, ForeignKey(
                'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

USER_GROUP_TABLE = Table(
    'usertousergroups', metadata,
    Column('username', Unicode(255), ForeignKey(
                'user.user_name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idgroup', Integer, ForeignKey(
                'usergroup.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

MAP_PERMISSION_TABLE = Table(
    'mappermissions', metadata,
    Column('idmap', Integer, ForeignKey(
                'map.idmap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

MAP_GROUP_TABLE = Table(
    'mapgroup', metadata,
    Column('idgroup', Integer, ForeignKey(
                'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idmap', Integer, ForeignKey(
                'map.idmap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)                           
)

SUB_MAP_NODE_MAP_TABLE = Table(
    'submapmapnodetable', metadata,
    Column('mapnodeid', Integer, ForeignKey(
                'mapnode.idmapnode',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idmap', Integer, ForeignKey(
                'map.idmap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)                           
)

HOST_HOSTCLASS_TABLE = Table(
    'host2hostclass', metadata,
    Column('hostname', Unicode(255), ForeignKey(
                'host.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idclass', Integer, ForeignKey(
                'hostclass.idclass',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

HOST_GROUP_TABLE = Table(
    'hostgroup', metadata,
    Column('idhost', Integer, ForeignKey(
                'host.idhost',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgroup', Integer, ForeignKey(
                'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

SERVICE_GROUP_TABLE = Table(
    'servicegroup', metadata,
    Column('idservice', Integer, ForeignKey(
                'service.idservice',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgroup', Integer, ForeignKey(
                'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

GRAPH_GROUP_TABLE = Table(
    'graphgroup', metadata,
    Column('idgraph', Integer, ForeignKey(
                'graph.idgraph',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgroup', Integer, ForeignKey(
                'group.idgroup',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

GRAPH_PERFDATASOURCE_TABLE = Table(
    'graphperfdatasource', metadata,
    Column('idperfdatasource', Integer, ForeignKey(
                'perfdatasource.idperfdatasource',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idgraph', Integer, ForeignKey(
                'graph.idgraph',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

