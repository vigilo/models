# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Host"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String

from ..vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

host = Table(bdd_basename + 'host',
        metadata,
        Column(u'name',
            String(length=255, convert_unicode=True, assert_unicode=None),
            index=True,primary_key=True, nullable=False),
        Column(u'checkhostcmd',
            String(length=255, convert_unicode=True, assert_unicode=None),
            primary_key=False, nullable=False),
        Column(u'community',
            String(length=255, convert_unicode=True, assert_unicode=None),
            primary_key=False, nullable=False),
        Column(u'fqhn',
            String(length=255, convert_unicode=True, assert_unicode=None),
            primary_key=False, nullable=False),
        Column(u'hosttpl',
            String(length=255, convert_unicode=True, assert_unicode=None),
            primary_key=False, nullable=False),
        Column(u'mainip',
            String(length=255, convert_unicode=True, assert_unicode=None),
            primary_key=False, nullable=False),
        Column(u'port', Integer(), primary_key=False, nullable=False),
        Column(u'snmpoidsperpdu', Integer(), primary_key=False),
        Column(u'snmpversion',
            String(length=255, convert_unicode=True, assert_unicode=None),
            primary_key=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

# Classe a mapper

class Host(object):
    
    """
    Classe liée avec la table associée
    """
    
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

mapper(Host, host)


