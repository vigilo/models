# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèles pour les tables SQL utilisées dans Vigilo."""

__all__ = [
    'EventHistory', 'Event', 'CorrEvent',
    'GraphGroup', 'Graph', 'Host', 'HostClass', 'PerfDataSource',
    'SupItem', 'LowLevelService', 'HighLevelService',
    'Dependency', 'Version', 'State', 'Permission',
    'UserGroup', 'User', 'Tag',
    'MapGroup', 'MapLink', 'MapNode', 'MapNodeHost', 'MapNodeHls',
    'Map', 'MapSegment', 'MapServiceLink', 'Legend', 'Service', 'StateName',
    'Application', 'VigiloServer', 'Ventilation',
    'ImpactedPath', 'ImpactedHLS', 'Downtime', 'DowntimeStatus',
    'FileDeployment', 'Change', 'ConfItem',  'MapNodeLls', 'MapNodeService',
]

from .eventhistory import EventHistory
from .event import Event
from .correvent import CorrEvent
from .graph import Graph
from .host import Host
from .hostclass import HostClass
from .perfdatasource import PerfDataSource
from .group import MapGroup, GraphGroup, SupItemGroup
from .supitem import SupItem
from .service import LowLevelService, HighLevelService, Service
from .dependency import Dependency
from .version import Version
from .state import State
from .statename import StateName
from .permission import Permission
from .datapermission import DataPermission
from .usergroup import UserGroup
from .user import User
from .tag import Tag
from .mapnode import MapNode, MapNodeHost, MapNodeService, \
        MapNodeHls, MapNodeLls
from .map import Map
from .maplink import MapLink, MapServiceLink, MapSegment, MapLlsLink, \
        MapHlsLink
from .legend import Legend
from .application import Application
from .impactedpath import ImpactedPath
from .impactedhls import ImpactedHLS
from .downtime import Downtime
from .downtimestatus import DowntimeStatus
from .vigiloserver import VigiloServer
from .ventilation import Ventilation
from .filedeployment import FileDeployment
from .change import Change
from .confitem import ConfItem
from .hlshistory import HLSHistory

# Spécifique projets
from pkg_resources import working_set
for entry in working_set.iter_entry_points("vigilo.models", "tables"):
    # Charge les tables spécifiques
    tables_ext = entry.load()
    # Importe toutes les tables spécifiques (comme ci-dessus)
    for t in tables_ext.__all__:
        globals()[t] = getattr(tables_ext, t)
        __all__.append(t)

