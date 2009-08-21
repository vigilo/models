# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table GroupPermissions"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, UnicodeText

from .vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

grouppermissions = Table(
    bdd_basename + 'grouppermissions',
    metadata,
    Column(u'groupname',
        UnicodeText(),
        ForeignKey(bdd_basename +'groups.name'),
        primary_key=True, nullable=False),
    Column(u'idpermission',
        Integer(), autoincrement=False, primary_key=True, nullable=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

# Classe a mapper

class GroupPermissions(object):
    
    """
    Classe liée avec la table associée
    """

    def __init__(self, groupname, idpermission = 0):
        self.groupname = groupname
        self.idpermission = idpermission

mapper(GroupPermissions, grouppermissions)
