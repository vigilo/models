# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table host_vigiloserver_appgroup"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import UnicodeText, Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('host_vigiloserver_appgroup', )

class Host_VigiloServer_AppGroup(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'host_vigiloserver_appgroup'

    hostname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + 'host.name'),
        primary_key=True, nullable=False)

    idsrv = Column(
        Integer,
        ForeignKey(bdd_basename + 'vigiloserver.idsrv'),
        primary_key=True, nullable=False)

    idappgroup = Column(
        Integer,
        ForeignKey(bdd_basename + 'appgroup.idappgroup'),
        primary_key=True, nullable=False)

