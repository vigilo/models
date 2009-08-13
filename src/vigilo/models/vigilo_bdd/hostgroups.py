# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table HostGroups"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import String

from ..vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

hostgroups = Table(bdd_basename + 'hostgroups',
    metadata,
    Column(u'hostname',
        String(length=100, convert_unicode=True, assert_unicode=None),
        ForeignKey(bdd_basename + u'host.name'),
        primary_key=True, nullable=False),
    Column(u'groupname',
        String(length=100, convert_unicode=True, assert_unicode=None),
        ForeignKey(bdd_basename + u'groups.name'),
        index=True ,primary_key=True, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

# Classe a mapper

class HostGroups(object):
    
    """
    Classe liée avec la table associée
    """
    
    def __init__(self, hostname, groupname):
        self.hostname = hostname
        self.groupname = groupname

mapper(HostGroups, hostgroups)


