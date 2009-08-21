# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Graph"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column
from sqlalchemy.types import UnicodeText

from .vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

graph =  Table(bdd_basename + 'graph',
        metadata,
        Column(u'name',
            UnicodeText(),
            primary_key=True, nullable=False),
        Column(u'template',
            UnicodeText(),
            nullable=False),
        Column(u'vlabel',
            UnicodeText(),
            nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

# Classe a mapper

class Graph(object):
    
    """
    Classe liée avec la table associée
    """
    
    def __init__(self, name, template = '', vlabel = ''):
        self.name = name
        self.template = template
        self.vlabel = vlabel
        
mapper(Graph, graph)
