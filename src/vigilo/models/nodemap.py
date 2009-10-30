# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
Modèle pour la table NodeMap

    @ival idnodemap: Identifiant du modèle de noeud (séquence) 
    @ival label: Label du noeud.
"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText, Boolean
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

from .secondary_tables import SEGMENT_NODE_TABLE, SUB_MAP_NODE_MAP_TABLE

__all__ = ('NodeMapHost', 'NodeMapService', 'NodeMapPerformance')

class NodeMap(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'nodemap'
    
    
    #id = Column(Integer, primary_key=True)

    
    idnodemap = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )
    
    label = Column(
    Unicode(255)               
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
    
    hidelabel = Column(
        Boolean, 
        default = False, nullable = False)

    map = relation('Map', back_populates='nodes')
    #primaryjoin='NodeMap.mapadress==Map.name'
    
    submaps = relation('Map', secondary=SUB_MAP_NODE_MAP_TABLE)
    #, primaryjoin='NodeMap.idnodemap==Map.nodeforsubmap'
    
    segments = relation('Segment', back_populates='nodemaps', secondary=SEGMENT_NODE_TABLE, lazy='dynamic', 
                        uselist=True)
    
    
    type_node = Column(
        'type_node',
        Unicode(16),
        nullable=False)

    __mapper_args__ = {'polymorphic_on': type_node}
    
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
    __mapper_args__ = {'polymorphic_identity': u'host'}
    #__mapper_args__ = {'concrete':True}
    
    idnodemaphost = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'nodemap.idnodemap',
            onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        nullable=False
    )
    
    name = Column(
        Unicode(255), 
        ForeignKey(
            bdd_basename + 'host.name',
            onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)
    #index=True,    
    hosticon = Column(
        Unicode(255)
        )
    
    hoststateicon = Column(
        Unicode(255)
        )
    
    

    
    
    def __init__(self, **kwargs):
        super(NodeMapHost, self).__init__(**kwargs)
        #self.type_node = u'host'
        
        
class NodeMapService(NodeMap):
    """
    Classe chargée de la représentation graphique d'un service dans vigimap 

    """
    __tablename__ = 'nodemapservice'
    __mapper_args__ = {'polymorphic_identity': u'service'}
    #__mapper_args__ = {'concrete':True}
    
    idnodemap = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'nodemap.idnodemap',
            onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True,
        nullable=False
    )
    
    name = Column(
        Unicode(255),
        ForeignKey(bdd_basename + 'service.name',
        ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    #index=True,
        
    serviceicon = Column(
        Unicode(255)
        )
    
    servicestateicon = Column(
        Unicode(255)
        )

    
    def __init__(self, **kwargs):
        super(NodeMapService, self).__init__(**kwargs)
        #self.type_node = u'service'

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

