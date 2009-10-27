# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table NodeMap"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, Boolean
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

from .secondary_tables import SEGMENT_NODE_TABLE

__all__ = ('NodeMapHost', 'NodeMapService', 'NodeMapPerformance')

class NodeMap(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'nodemap'
        
    idnodemap = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )

    isvisiblename = Column(Boolean)
    
    isvisibleinventory = Column(Boolean)
    
    mapadress = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'map.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    
    x_pos = Column(Integer, nullable=False)
    
    y_pos = Column(Integer, nullable=False)

    maps = relation('Map', back_populates='nodes')
    
    submaps = relation('Map', 
                    uselist=True)
    
    segments = relation('Segment', back_populates='nodemaps', secondary=SEGMENT_NODE_TABLE, lazy='dynamic', 
                        uselist=True)
    
    
    type_node = Column(
        'type_node',
        Unicode(16),
        nullable=False)

    #pour le moment on teste l'héritage en tables concretes
    # __mapper_args__ = {'polymorphic_on': type_node}


    def __init__(self, **kwargs):
        """Initialise un node."""
        super(NodeMap, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Node} pour l'afficher dans les formulaires.

        Le nom du noeud est utilisé pour le représenter dans les formulaires.

        @return: Le nom du node.
        @rtype: C{str}
        """
        return self.name


class NodeMapHost(NodeMap):
    """
    Classe chargée de la représentation graphique d'un hôte dans vigimap 

    """
    __tablename__ = 'nodemaphost'
    __mapper_args__ = {'concrete':True}
    
    idnodemaphost = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )
    
    name = Column(
        Unicode(255), 
        ForeignKey(
            bdd_basename + 'host.name',
            onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)
    #index=True,    
    hosticon = Column(
        Unicode(255),
        nullable=False)
    
    hoststateicon = Column(
        Unicode(255),
        nullable=False)
    
    hidelabel = Column(
        Boolean, 
        default = False, nullable = False)
    
    def __init__(self, **kwargs):
        super(NodeMapHost, self).__init__(**kwargs)
        self.type_node = u'host'
        
        
class NodeMapService(NodeMap):
    """
    Classe chargée de la représentation graphique d'un service dans vigimap 

    """
    __tablename__ = 'nodemapservice'
    __mapper_args__ = {'concrete':True}
    
    idnodemapservice = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )
    
    name = Column(
        Unicode(255),
        ForeignKey(bdd_basename + 'service.name',
        ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    #index=True,
        
    serviceicon = Column(
        Unicode(255),
        nullable=False)
    
    servicestateicon = Column(
        Unicode(255),
        nullable=False)
    
    def __init__(self, **kwargs):
        super(NodeMapService, self).__init__(**kwargs)
        self.type_node = u'service'

"""        
class NodeMapPerformance(NodeMap):
    
    Classe chargée de la représentation graphique d'un modèle Performance dans vigimap 

    
    __mapper_args__ = {'concrete':True}
    TODO: Foreighkey inexistante pour l'instant
    name = Column(
        Unicode(255),
        index=True, ForeignKey(bdd_basename + 'service.name'),
        ondelete='CASCADE', onupdate='CASCADE',
        nullable=False)
        
    graphe = Column(
        Unicode(255),
        nullable=False)
    
    
    def __init__(self, **kwargs):
        super(NodeMapService, self).__init__(**kwargs)
        self.type_node = u'performance'
"""        

