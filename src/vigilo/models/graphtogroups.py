# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table GraphToGroups"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import UnicodeText

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('GraphToGroups', )

class GraphToGroups(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'graphtogroups'

    graphname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + 'graph.name'),
        primary_key=True, nullable=False)
    groupname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + \
                'graphgroup.name'),
        primary_key=True, nullable=False)

    def __init__(self, **kwargs):
        super(GraphToGroups, self).__init__(**kwargs)

