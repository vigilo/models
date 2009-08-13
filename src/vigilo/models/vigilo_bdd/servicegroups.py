# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table ServiceGroups"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import String

from ..vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

servicegroups =  Table(
    bdd_basename + 'servicegroups',
    metadata,
    Column(u'servicename',
        String(length=100, convert_unicode=True, assert_unicode=None),
        ForeignKey(
            bdd_basename + u'service.name'
        ), primary_key=True, nullable=False),
    Column(u'groupname',
        String(length=100, convert_unicode=True, assert_unicode=None),
        ForeignKey(
            bdd_basename + u'groups.name'
        ), index=True, primary_key=True, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

# Classe a mapper

class ServiceGroups(object):
    
    """
    Classe liée avec la table associée
    """
    
    def __init__(self, servicename, groupname):
        self.servicename = servicename
        self.groupname = groupname

mapper(ServiceGroups, servicegroups)


