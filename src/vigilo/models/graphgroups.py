# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table GraphGroups"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, UnicodeText

from .vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

graphgroups = Table(bdd_basename + 'graphgroups',
        metadata,
        Column(u'name',
            UnicodeText(),
            primary_key=True, nullable=False),
        Column(u'parent', Integer(), nullable=True),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

# Classe a mapper

class GraphGroups(object):
    """
    Classe liée avec la table associée
    """
    
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

mapper(GraphGroups, graphgroups)
