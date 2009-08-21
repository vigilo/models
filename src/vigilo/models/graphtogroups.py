# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table GraphToGroups"""
from __future__ import absolute_import

from sqlalchemy.orm import mapper
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase





class GraphToGroups(DeclarativeBase):
    __tablename__ = bdd_basename + 'graphtogroups'

    graphname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + 'graph.name'),
        primary_key=True, nullable=False)
    groupname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + \
                'graphgroups.name'),
        primary_key=True, nullable=False)

