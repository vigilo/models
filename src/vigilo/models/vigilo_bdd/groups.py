# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Groups"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column
from sqlalchemy.types import String

from ..vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

groups =  Table(bdd_basename + 'groups',
        metadata,
        Column(u'name',
            String(length=100, convert_unicode=True, assert_unicode=None),
            primary_key=True, nullable=False),
        Column(u'parent',
            String(length=100, convert_unicode=True, assert_unicode=None),
            index=True, primary_key=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

# Classe a mapper

class Groups(object):
    
    """
    Classe liée avec la table associée
    """
    
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent

mapper(Groups, groups)
