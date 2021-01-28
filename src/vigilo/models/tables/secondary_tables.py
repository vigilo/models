# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2021 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""
Contient les tables intermédiaires utilisées dans les relations de type
"plusieurs-à-plusieurs" sans attributs propres.
Les tables définies ci-dessous ne correspondent qu'à des relations binaires.
Si vous devez représenter une relation ternaire (ou plus), créez une
table spécifique dans le reste du modèle (ie. : une classe qui hérite
de DeclarativeBase).
"""

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.types import Unicode, Integer
from vigilo.models.session import metadata

USERGROUP_PERMISSION_TABLE = Table(
    'vigilo_usergrouppermissions', metadata,
    Column(
        'idgroup',
        Integer,
        ForeignKey(
            'vigilo_usergroup.idgroup',
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
            'vigilo_permission.idpermission',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
)

EVENTSAGGREGATE_TABLE = Table(
    'vigilo_eventsaggregate', metadata,
    Column(
        'idevent',
        Integer,
        ForeignKey(
            'vigilo_event.idevent',
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
            'vigilo_correvent.idcorrevent',
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
    'vigilo_usertousergroups', metadata,
    Column(
        'username',
        Unicode(255),
        ForeignKey(
            'vigilo_user.user_name',
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
            'vigilo_usergroup.idgroup',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
)

MAP_GROUP_TABLE = Table(
    'vigilo_mapgroup', metadata,
    Column(
        'idgroup',
        Integer,
        ForeignKey(
            'vigilo_group.idgroup',
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
            'vigilo_map.idmap',
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
    'vigilo_submaps', metadata,
    Column(
        'idmapnode',
        Integer,
        ForeignKey(
            'vigilo_mapnode.idmapnode',
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
            'vigilo_map.idmap',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
)

HOST_HOSTCLASS_TABLE = Table(
    'vigilo_host2hostclass', metadata,
    Column(
        'idhost',
        Integer,
        ForeignKey(
            'vigilo_host.idhost',
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
            'vigilo_hostclass.idclass',
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
    'vigilo_supitemgroup', metadata,
    Column(
        'idsupitem',
        Integer,
        ForeignKey(
            'vigilo_supitem.idsupitem',
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
            'vigilo_group.idgroup',
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
    'vigilo_graphgroup', metadata,
    Column(
        'idgraph',
        Integer,
        ForeignKey(
            'vigilo_graph.idgraph',
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
            'vigilo_group.idgroup',
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
    'vigilo_graphperfdatasource', metadata,
    Column(
        'idperfdatasource',
        Integer,
        ForeignKey(
            'vigilo_perfdatasource.idperfdatasource',
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
            'vigilo_graph.idgraph',
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
    'vigilo_silencestate', metadata,
    Column(
        'idsilence',
        Integer,
        ForeignKey(
            'vigilo_silence.idsilence',
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
            'vigilo_statename.idstatename',
            onupdate="CASCADE",
            ondelete="CASCADE",
            deferrable=True,
            initially='IMMEDIATE',
        ),
        primary_key=True,
    ),
)

