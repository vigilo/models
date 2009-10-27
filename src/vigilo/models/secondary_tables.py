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
    Column('groupname', Unicode(255), ForeignKey(
                bdd_basename + 'usergroup.group_name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                bdd_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
)

HOST_TAG_TABLE = Table(
    bdd_basename + 'tags2hosts', metadata,
    Column('hostname', Unicode(255), ForeignKey(
                bdd_basename + 'host.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('name', Unicode(255), ForeignKey(
                bdd_basename + 'tag.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

SERVICE_TAG_TABLE = Table(
    bdd_basename + 'tags2services', metadata,
    Column('servicename', Unicode(255), ForeignKey(
                bdd_basename + 'service.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('name', Unicode(255), ForeignKey(
                bdd_basename + 'tag.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

EVENTS_EVENTSAGGREGATE_TABLE = Table(
    bdd_basename + 'eventsaggregates2events', metadata,
    Column('idevent', Unicode(40), ForeignKey(
                bdd_basename + 'event.idevent',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idaggregate', Unicode(40), ForeignKey(
                bdd_basename + 'eventsaggregate.idaggregate',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
)

EVENTSAGGREGATE_HLS_TABLE = Table(
    bdd_basename + 'eventsaggregate2hls', metadata,
    Column('hls_servicename', Unicode(255),
            ForeignKey(bdd_basename + 'highlevelservice.servicename'),
            primary_key=True),
    Column('idaggregate', Unicode(40), ForeignKey(
                bdd_basename + 'eventsaggregate.idaggregate',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
)

GROUP_PERMISSION_TABLE = Table(
    bdd_basename + 'grouppermissions', metadata,
    Column('groupname', Unicode(255), ForeignKey(
                bdd_basename + 'group.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
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
    Column('groupname', Unicode(255), ForeignKey(
                bdd_basename + 'usergroup.group_name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)

SEGMENT_NODE_TABLE = Table(
    bdd_basename + 'segmentnodetable', metadata,
    Column('idsegment', Integer, ForeignKey(
                bdd_basename + 'segment.idsegment',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False),
    Column('idnodemap', Integer, ForeignKey(
                bdd_basename + 'nodemap.idnodemap',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

MAP_GROUP_PERMISSION_TABLE = Table(
    bdd_basename + 'mapgrouppermissions', metadata,
    Column('mapgroupname', Unicode(255), ForeignKey(
                bdd_basename + 'mapgroup.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                bdd_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)

MAP_GROUP_MAP_TABLE = Table(
    bdd_basename + 'mapgroupmaptable', metadata,
    Column('mapgroupname', Unicode(255), ForeignKey(
                bdd_basename + 'mapgroup.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('mapname', Unicode(255), ForeignKey(
                bdd_basename + 'map.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)                           
)

"""
MAP_LINK_TABLE = Table(
    bdd_basename + 'maplinktable', metadata,
    Column('groupname', Unicode, ForeignKey(
                bdd_basename + 'group.name',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idpermission', Integer, ForeignKey(
                bdd_basename + 'permission.idpermission',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True, autoincrement=False)
)
"""


