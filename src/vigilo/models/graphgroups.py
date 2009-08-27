# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table GraphGroups"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

class GraphGroups(DeclarativeBase):
    __tablename__ = bdd_basename + 'graphgroups'

    name = Column(
            UnicodeText,
            primary_key=True)
    parent = Column(Integer, nullable=True)

