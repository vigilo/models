# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table State"""

from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column, DefaultClause, ForeignKey
from sqlalchemy.types import Integer, UnicodeText, Text, DateTime

from sqlalchemy.databases.mysql import MSEnum

from datetime import datetime

from .vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

state = Table(bdd_basename + 'state', metadata,
    Column(u'idstat', Integer(), primary_key=True, nullable=False,
        autoincrement=True),
    Column(u'hostname',
        UnicodeText(),
        ForeignKey(bdd_basename +'host.name'),
        index=True, nullable=False),
    Column(u'servicename',
        UnicodeText(),
        ForeignKey(bdd_basename + 'service.name'),
        index=True),
    Column(u'ip',
        UnicodeText()),
    Column(u'timestamp', DateTime(timezone=False)),
    Column(u'statename', MSEnum('WARNING','OK','CRITICAL','UNKNOWN'),
        nullable=False,
        server_default=DefaultClause('OK', for_update=False)),
    Column(u'type', MSEnum('SOFT','HARD'),
        nullable=False,
        server_default=DefaultClause('SOFT', for_update=False)),
    Column(u'attempt', Integer(), nullable=False,
        autoincrement=False),
    Column(u'message',
        Text(length=None, convert_unicode=True, assert_unicode=None)),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

# Classe a mapper

class State(object):
    
    """
    Classe liée avec la table associée
    """

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

mapper(State, state)
