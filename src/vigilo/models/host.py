# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Host"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase



class Host(DeclarativeBase):
    __tablename__ = bdd_basename + 'host'

    name = Column(
        UnicodeText(),
        index=True,primary_key=True, nullable=False)
    checkhostcmd = Column(
        UnicodeText(),
        nullable=False)
    community = Column(
        UnicodeText(),
        nullable=False)
    fqhn = Column(
        UnicodeText(),
        nullable=False)
    hosttpl = Column(
        UnicodeText(),
        nullable=False)
    mainip = Column(
        UnicodeText(),
        nullable=False)
    port = Column( Integer(), nullable=False)
    snmpoidsperpdu = Column( Integer())
    snmpversion = Column(
        UnicodeText())

    def __init__(self, name, checkhostcmd = '', community = '', fqhn = '',
            hosttpl = '', mainip = '', port = 0, snmpoidsperdu = 0,
            snmpversion = ''):
        self.name = name
        self.checkhostcmd = checkhostcmd
        self.community = community
        self.fqhn = fqhn
        self.hosttpl = hosttpl
        self.mainip = mainip
        self.port = port
        self.snmpoidsperdu = snmpoidsperdu
        self.snmpversion = snmpversion




