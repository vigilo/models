# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table GroupPermissions"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase



class GroupPermissions(DeclarativeBase):
    __tablename__ = bdd_basename + 'grouppermissions'

    groupname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename +'groups.name'),
        primary_key=True, nullable=False)
    idpermission = Column(
        Integer(),
        ForeignKey(bdd_basename + 'permission.idpermission'),
        default=0,
        autoincrement=False, primary_key=True, nullable=False)

