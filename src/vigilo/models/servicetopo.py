# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceTopo"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import UnicodeText

from .vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

servicetopo =  Table(bdd_basename + 'servicetopo',
    metadata,
    Column(u'servicename',
        UnicodeText(),
        ForeignKey(bdd_basename + \
                u'service.name'),
        primary_key=True, nullable=False),
    Column(u'function',
        UnicodeText(),
        primary_key=False, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

# Classe a mapper

class ServiceTopo(object):
    
    """
    Classe liée avec la table associée
    """
    
    def __init__(self, servicename, function=''):
        self.servicename = servicename
        self.function = function

mapper(ServiceTopo, servicetopo)
