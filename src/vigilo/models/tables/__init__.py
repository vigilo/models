# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2020 CS GROUP - France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèles pour les tables SQL utilisées dans Vigilo."""

__all__ = [
    'EventHistory', 'Event', 'CorrEvent', 'ConfFile',
    'GraphGroup', 'Graph', 'Host', 'HostClass', 'PerfDataSource',
    'SupItem', 'LowLevelService', 'HighLevelService',
    'HLSPriority', 'HLSHistory',
    'Dependency', 'DependencyGroup', 'Version', 'State', 'Permission',
    'UserGroup', 'User', 'Tag', 'SupItemGroup',
    'MapGroup', 'MapLink', 'MapNode', 'MapNodeHost', 'MapNodeHls',
    'Map', 'MapSegment', 'MapServiceLink', 'Legend', 'Service', 'StateName',
    'Application', 'VigiloServer', 'Ventilation',
    'ImpactedPath', 'ImpactedHLS', 'Silence',
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
from .dependencygroup import DependencyGroup
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
from .silence import Silence
from .vigiloserver import VigiloServer
from .ventilation import Ventilation
from .filedeployment import FileDeployment
from .change import Change
from .confitem import ConfItem
from .conffile import ConfFile
from .hlshistory import HLSHistory
from .hlspriority import HLSPriority

# Importation des vues.
from .grouppath import GroupPath
from .usersupitem import UserSupItem
from .guieventduration import GuiEventDuration

# Spécifique projets
from pkg_resources import working_set
for entry in working_set.iter_entry_points("vigilo.models", "tables"):
    # Charge les tables spécifiques
    tables_ext = entry.load()
    # Importe toutes les tables spécifiques (comme ci-dessus)
    for t in tables_ext.__all__:
        globals()[t] = getattr(tables_ext, t)
        __all__.append(t)
