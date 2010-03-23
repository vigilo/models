# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèles pour les tables SQL utilisées dans Vigilo."""

__all__ = (
    'VIGILO_MODEL_VERSION',
    'EventHistory', 'Event', 'CorrEvent',
    'GraphGroup', 'Graph', 'HostGroup', 'Host', 'HostClass',
    'PerfDataSource', 'ServiceGroup',
    'SupItem', 'LowLevelService', 'HighLevelService',
    'Dependency', 'Version', 'State', 'Permission',
    'UserGroup', 'User', 'BoardViewFilter', 'CustomGraphView', 'Tag',
    'MapGroup', 'MapLink', 'MapNode', 'MapNodeHost',
    'Map', 'MapSegment', 'MapServiceLink', 'Legend', 'Service', 'StateName',
    'Application', 'VigiloServer', 'Ventilation', 'Installation',
    'ImpactedPath', 'ImpactedHLS', 'Downtime', 'DowntimeStatus',
    'FileDeployment', 'Change', 'ConfItem'
)

# Numéro de version du modèle, il sera incrémenté pour chaque nouvelle
# version livrée au client. Il sera utilisé par les scripts de mise à jour
# de Vigilo afin d'importer les données d'une ancienne version du modèle
# vers la nouvelle version (permet d'assurer la rétro-compatibilité).
VIGILO_MODEL_VERSION = 1


from .eventhistory import EventHistory
from .event import Event
from .correvent import CorrEvent
from .graph import Graph
from .host import Host
from .hostclass import HostClass
from .perfdatasource import PerfDataSource
from .group import HostGroup, ServiceGroup, MapGroup, GraphGroup
from .supitem import SupItem
from .service import LowLevelService, HighLevelService, Service
from .dependency import Dependency
from .version import Version
from .state import State
from .statename import StateName
from .permission import Permission
from .usergroup import UserGroup
from .user import User
from .boardviewfilter import BoardViewFilter
from .customgraphview import CustomGraphView
from .tag import Tag
from .mapnode import MapNode, MapNodeHost, MapNodeService
from .map import Map
from .maplink import MapLink, MapServiceLink, MapSegment
from .legend import Legend
from .application import Application
from .impactedpath import ImpactedPath
from .impactedhls import ImpactedHLS
from .downtime import Downtime
from .downtimestatus import DowntimeStatus
from .vigiloserver import VigiloServer
from .ventilation import Ventilation
from .installation import Installation
from .filedeployment import FileDeployment
from .change import Change
from .confitem import ConfItem
