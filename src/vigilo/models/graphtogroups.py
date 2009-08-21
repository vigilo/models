# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table GraphToGroups"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import String

from .vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

graphtogroups =  Table(
    bdd_basename + 'graphtogroups',
    metadata,
    Column(u'graphname',
        String(length=100, convert_unicode=False, assert_unicode=None),
        ForeignKey(bdd_basename + 'graph.name'),
        primary_key=True, nullable=False),
    Column(u'groupname',
        String(length=100, convert_unicode=False, assert_unicode=None),
        ForeignKey(bdd_basename + \
                'graphgroups.name'),
        primary_key=True, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

# Classe a mapper

class GraphToGroups(object):
    """
    Classe liée avec la table associée
    """
    
    def __init__(self, graphname, groupname):
        self.graphname = graphname
        self.groupname = groupname


mapper(GraphToGroups, graphtogroups)
