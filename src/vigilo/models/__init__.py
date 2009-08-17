# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
BdD Vigilo initialisation
"""

from sqlalchemy.ext.declarative import declarative_base

DeclarativeBase = declarative_base()

metadata = DeclarativeBase.metadata

from .vigilo_bdd import EventHistory, Events, GraphGroups, Graph, Groups, \
        GroupPermissions, HostGroups, Host, PerfDataSource, ServiceGroups, \
        ServiceHautNiveau, Service, ServiceTopo, GraphToGroups, Version, State
