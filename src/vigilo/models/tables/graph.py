# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Graph"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import GRAPH_GROUP_TABLE
from vigilo.models.tables.secondary_tables import GRAPH_PERFDATASOURCE_TABLE

__all__ = ('Graph', )

class Graph(DeclarativeBase, object):
    """
    Informations sur une datasource d'un service.
    
    @ivar idgraph: Identifiant du graph, autogénéré.
    @ivar name: Nom du graph.
    @ivar template: Le type de graphe généré par rrdtool (ligne, barres,
        barres cumulés, etc.).
    @ivar vlabel: Unité de mesure (bits/s, Mbits/s ...).
    @ivar groups: Liste des groupes de graphes auxquels ce graphe appartient.
    @ivar perfdatasources: Liste des sources de données de performances
        rattachées à ce graphe.
    """
    __tablename__ = 'graph'
    
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
    
    perfdatasources = relation('PerfDataSource', lazy=True,
        back_populates='graphs', secondary=GRAPH_PERFDATASOURCE_TABLE)


    def __init__(self, **kwargs):
        super(Graph, self).__init__(**kwargs)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return "<%s \"%s\">" % (self.__class__.__name__, str(self.name))

