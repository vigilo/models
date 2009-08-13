# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
BdD Vigilo initialisation
"""

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from vigilo.common.conf import settings

maker = sessionmaker(autoflush=True, autocommit=False,
                             extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

DeclarativeBase = declarative_base()

metadata = DeclarativeBase.metadata

engine = create_engine(settings['VIGILO_MODELS'], echo=True)

DBSession.configure(bind=engine)

from .vigilo_bdd import EventHistory, Events, GraphGroups, Graph, Groups, \
        GroupPermissions, HostGroups, Host, PerfDataSource, ServiceGroups, \
        ServiceHautNiveau, Service, ServiceTopo, GraphToGroups, Version, State
