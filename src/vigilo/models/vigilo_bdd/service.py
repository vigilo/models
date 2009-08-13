# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Service"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column
from sqlalchemy.types import String

from ..vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

service =  Table(bdd_basename + 'service',
        metadata,
        Column(u'name',
            String(length=255, convert_unicode=True, assert_unicode=None),
            index=True, primary_key=True, nullable=False),
        Column(u'type',
            String(length=255, convert_unicode=True, assert_unicode=None),
            primary_key=False, nullable=False),
        Column(u'command',
            String(length=255, convert_unicode=True, assert_unicode=None),
            primary_key=False, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

# Classe a mapper

class Service(object):
    
    """
    Classe liée avec la table associée
    """
    
    def __init__(self, name, servicetype = 0, command = ''):
        self.name = name
        self.type = servicetype
        self.command = command
      
mapper(Service, service)


