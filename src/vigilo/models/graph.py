# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Graph"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Unicode

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('Graph', )

class Graph(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'graph'

    name = Column(
        Unicode(255),
        primary_key=True, nullable=False)

    template = Column(
        Unicode(255),
        default=u'', nullable=False)

    vlabel = Column(
        Unicode(255),
        default=u'', nullable=False)


    def __init__(self, **kwargs):
        super(Graph, self).__init__(**kwargs)

    def __unicode__(self):
        return self.name

