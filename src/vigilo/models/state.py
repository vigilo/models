# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table State"""

from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column, DefaultClause, ForeignKey
from sqlalchemy.types import Integer, UnicodeText, Text, DateTime

from sqlalchemy.databases.mysql import MSEnum

from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase


class State(DeclarativeBase):

    __tablename__ = bdd_basename + 'state'

    idstat = Column( Integer(), primary_key=True, nullable=False,
        autoincrement=True)
    hostname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename +'host.name'),
        index=True, nullable=False)
    servicename = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + 'service.name'),
        index=True)
    ip = Column(
        UnicodeText())
    timestamp = Column( DateTime(timezone=False))
    statename = Column( MSEnum('WARNING','OK','CRITICAL','UNKNOWN'),
        nullable=False,
        server_default=DefaultClause('OK', for_update=False))
    type = Column( MSEnum('SOFT','HARD'),
        nullable=False,
        server_default=DefaultClause('SOFT', for_update=False))
    attempt = Column( Integer(), nullable=False,
        autoincrement=False)
    message = Column(
        Text(length=None, convert_unicode=True, assert_unicode=None))

    def __init__(self, hostname, servicename, ip, timestamp = datetime.now(),
            statename = 'OK', type = 'SOFT', attempt = 1, message = ''):

        self.hostname = hostname
        self.servicename = servicename
        self.ip = ip
        self.timestamp = timestamp
        self.statename = statename
        self.type = type
        self.attempt = attempt
        self.message = message

