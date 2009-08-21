# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceHautNiveau"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import String

from .vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

servicehautniveau = Table(
    bdd_basename + 'servicehautniveau',
    metadata,
    Column(u'servicename',
        String(length=100, convert_unicode=True, assert_unicode=None),
        ForeignKey(
            bdd_basename + u'service.name'
        ), primary_key=True, nullable=False),
    Column(u'servicename_dep',
        String(length=100, convert_unicode=True, assert_unicode=None),
        ForeignKey(
            bdd_basename + u'service.name'
        ), index=True ,primary_key=True, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

# Classe a mapper

class ServiceHautNiveau(object):
    
    """
    Classe liée avec la table associée
    """
    
    def __init__(self, servicename, servicename_dep):
        self.servicename = servicename
        self.servicename_dep = servicename_dep

mapper(ServiceHautNiveau, servicehautniveau)
