# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Graph"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .secondary_tables import GRAPH_GROUP_TABLE
from sqlalchemy.orm import relation

__all__ = ('Graph', )

class Graph(DeclarativeBase, object):
    """
    Informations sur une datasource d'un service.
    
    @ivar idgraph: Identifiant du graph, autogénéré.
    @ivar name: Nom du graph.
    @ivar template: XXX.
    @ivar vlabel: Unité de mesure (bits/s, Mbits/s ...).
    """
    __tablename__ = bdd_basename + 'graph'
    
    idgraph = Column(
        Integer,
        primary_key=True, autoincrement=True,)

    name = Column(
        Unicode(255),
        nullable=False)

    template = Column(
        Unicode(255),
        default=u'', nullable=False)
    
    vlabel = Column(
        Unicode(255),
        default=u'', nullable=False)
    
    groups = relation('GraphGroup', secondary=GRAPH_GROUP_TABLE,
                            back_populates='graphs')
    
    perfdatasources = relation('PerfDataSource', secondary=GRAPH_PERFDATASOURCE_TABLE,
                         back_populates='graphs', lazy=True)


    def __init__(self, **kwargs):
        super(Graph, self).__init__(**kwargs)

    def __unicode__(self):
        return self.name

