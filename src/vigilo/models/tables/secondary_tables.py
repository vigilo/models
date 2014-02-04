# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2014 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

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
from vigilo.models.session import metadata, ForeignKey, Table

USERGROUP_PERMISSION_TABLE = Table(
    'usergrouppermissions', metadata,
    Column(
        'idgroup',
        Integer,
        ForeignKey(
            'usergroup.idgroup',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
    Column(
        'idpermission',
        Integer,
        ForeignKey(
            'permission.idpermission',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
)

EVENTSAGGREGATE_TABLE = Table(
    'eventsaggregate', metadata,
    Column(
        'idevent',
        Integer,
        ForeignKey(
            'event.idevent',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
    Column(
        'idcorrevent',
        Integer,
        ForeignKey(
            'correvent.idcorrevent',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
)

USER_GROUP_TABLE = Table(
    'usertousergroups', metadata,
    Column(
        'username',
        Unicode(255),
        ForeignKey(
            'user.user_name',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
    Column(
        'idgroup',
        Integer,
        ForeignKey(
            'usergroup.idgroup',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
)

MAP_GROUP_TABLE = Table(
    'mapgroup', metadata,
    Column(
        'idgroup',
        Integer,
        ForeignKey(
            'group.idgroup',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
    Column(
        'idmap',
        Integer,
        ForeignKey(
            'map.idmap',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
)

SUB_MAP_NODE_MAP_TABLE = Table(
    'submaps', metadata,
    Column(
        'idmapnode',
        Integer,
        ForeignKey(
            'mapnode.idmapnode',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
    Column(
        'idmap',
        Integer,
        ForeignKey(
            'map.idmap',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
)

HOST_HOSTCLASS_TABLE = Table(
    'host2hostclass', metadata,
    Column(
        'idhost',
        Integer,
        ForeignKey(
            'host.idhost',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
    Column(
        'idclass',
        Integer,
        ForeignKey(
            'hostclass.idclass',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
)

SUPITEM_GROUP_TABLE = Table(
    'supitemgroup', metadata,
    Column(
        'idsupitem',
        Integer,
        ForeignKey(
            'supitem.idsupitem',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
    Column(
        'idgroup',
        Integer,
        ForeignKey(
            'group.idgroup',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
)

GRAPH_GROUP_TABLE = Table(
    'graphgroup', metadata,
    Column(
        'idgraph',
        Integer,
        ForeignKey(
            'graph.idgraph',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
    Column(
        'idgroup',
        Integer,
        ForeignKey(
            'group.idgroup',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
)

GRAPH_PERFDATASOURCE_TABLE = Table(
    'graphperfdatasource', metadata,
    Column(
        'idperfdatasource',
        Integer,
        ForeignKey(
            'perfdatasource.idperfdatasource',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
    Column(
        'idgraph',
        Integer,
        ForeignKey(
            'graph.idgraph',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
        autoincrement=False,
    ),
)

SILENCE_STATE_TABLE = Table(
    'silencestate', metadata,
    Column(
        'idsilence',
        Integer,
        ForeignKey(
            'silence.idsilence',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
    Column(
        'idstate',
        Integer,
        ForeignKey(
            'statename.idstatename',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
)

