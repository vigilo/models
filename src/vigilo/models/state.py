# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table State"""

from __future__ import absolute_import

from sqlalchemy import Column, DefaultClause, ForeignKey
from sqlalchemy.types import Integer, UnicodeText, Text, DateTime, Unicode

from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase


class State(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'state'

    idstate = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True)

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename +'host.name'),
        index=True, nullable=False)

    servicename = Column(
        Unicode(255),
        ForeignKey(bdd_basename + 'service.name'),
        index=True)

    ip = Column(Unicode(15))

    timestamp = Column(DateTime(timezone=False))

    statename = Column(
        Unicode(16),
        nullable=False,
        server_default=DefaultClause('OK', for_update=False))

    statetype = Column(Unicode(8),
        nullable=False,
        server_default=DefaultClause('SOFT', for_update=False))

    attempt = Column(
        Integer,
        nullable=False, autoincrement=False)

    message = Column(
        Text(length=None, convert_unicode=True, assert_unicode=None))

    def __init__(self, **kwargs):
        """Intiialise un état."""
        DeclarativeBase.__init__(self, **kwargs)

