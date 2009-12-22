# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
Modèle pour la table MapNode
"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, Boolean
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

from .secondary_tables import SUB_MAP_NODE_MAP_TABLE

__all__ = ('MapNodeHost', 'MapNodeService', 'MapNodePerformance')

class MapNode(DeclarativeBase, object):
    """
    @ivar idmapnode: Identifiant du modèle de noeud (séquence). 
    @ivar label: Label du noeud.
    @ivar x_pos: Position X.
    @ivar y_pos: Position Y.
    @ivar minimize: Booléen indiquant l'action à effectuer.
    @ivar type_node: Le type de noeud, peut etre
        'host', 'service',  ou 'performance'.
    @ivar idmap: Référence vers un identifiant de carte.
    @ivar map: Relation vers la carte du noeud.
    @ivar submaps: Liste des sous-cartes associées au noeud.
    """
    __tablename__ = bdd_basename + 'mapnode'

    idmapnode = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )
    
    label = Column(Unicode(255))

    idmap = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'map.idmap',
            onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    
    x_pos = Column(Integer, nullable=True)
    
    y_pos = Column(Integer, nullable=True)
    
    minimize = Column(
        Boolean, 
        default = False,
        nullable = False)

    map = relation('Map', back_populates='nodes')
    
    submaps = relation('Map', secondary=SUB_MAP_NODE_MAP_TABLE)
    
    type_node = Column('type_node', Unicode(16), nullable=False)

    __mapper_args__ = {'polymorphic_on': type_node}
    

    def __init__(self, **kwargs):
        """Initialise un noeud."""
        super(MapNode, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Node} pour l'afficher dans les formulaires.

        Le nom du noeud est utilisé pour le représenter dans les formulaires.

        @return: Le nom du node.
        @rtype: C{str}
        """
        return self.name


class MapNodeHost(MapNode):
    """
    Classe chargée de la représentation graphique d'un hôte dans vigimap
    
    @ivar idmapnode: Identifiant du modèle de l'hôte (séquence). 
    @ivar name: Nom de l'hôte.
    @ivar hosticon: Nom de l'icône de l'hôte. 
    @ivar hoststateicon: Etat de l'icône de l'hôte.
    """
    __tablename__ = 'mapnodehost'
    __mapper_args__ = {'polymorphic_identity': u'host'}
    
    idmapnode = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'mapnode.idmapnode',
            onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        nullable=False
    )
    
    idhost = Column(
        Integer, 
        ForeignKey(
            bdd_basename + 'host.idhost',
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
        super(MapNodeHost, self).__init__(**kwargs)
        #self.type_node = u'host'
        
        
class MapNodeService(MapNode):
    """
    Classe chargée de la représentation graphique d'un service dans vigimap 
    La représentation d'un service dans une carte se caractérise par un couple hôte-service.
    @ivar idmapnode: Identifiant du modèle de service (séquence). 
    @ivar hostname: Nom de l'hôte du noeud.
    @ivar servicename: Nom du service du noeud. 
    @ivar serviceicon: Nom de l'icône du service.
    @ivar servicestateicon: Etat de l'icône du service.
    """
    __tablename__ = 'mapnodeservice'
    __mapper_args__ = {'polymorphic_identity': u'service'}
    #__mapper_args__ = {'concrete':True}
    
    idmapnode = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'mapnode.idmapnode',
            onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True,
        nullable=False
    )

    idservice = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'servicelowlevel.idservice',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    service = relation('ServiceLowLevel')

    serviceicon = Column(
        Unicode(255)
        )
    
    servicestateicon = Column(
        Unicode(255)
        )

    
    def __init__(self, **kwargs):
        super(MapNodeService, self).__init__(**kwargs)
        #self.type_node = u'service'

"""
TODO: Classe en préparation
class MapNodePerformance(MapNode):
    
    Classe chargée de la représentation graphique d'un modèle Performance dans vigimap 

    __mapper_args__ = {'polymorphic_identity': u'performance'}
    
    idmapnode = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'mapnode.idmapnode',
            onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True,
        nullable=False
    )
    
    name = Column(
        Unicode(255),
        index=True, ForeignKey(bdd_basename + 'performance.name'),
        ondelete='CASCADE', onupdate='CASCADE',
        nullable=False)     
    
    
    def __init__(self, **kwargs):
        super(MapNodeService, self).__init__(**kwargs)
        #self.type_node = u'performance'
"""        

