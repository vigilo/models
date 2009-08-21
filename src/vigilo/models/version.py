# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Version"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, Column
from sqlalchemy.types import Integer, String

from .vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

version = Table(bdd_basename + 'version',
        metadata,
        Column(u'name',
            String(length=255, convert_unicode=True, assert_unicode=None),
            index=True,primary_key=True, nullable=False),
        Column(u'version',
            String(length=255, convert_unicode=True, assert_unicode=None),
            primary_key=False, nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
    )

# Classe a mapper

class Version(object):
    
    """
    Classe liée avec la table associée
    """
    
    pass

mapper(Version, version)


