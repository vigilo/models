# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
Modèle pour la table MapNode
"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, Boolean
from sqlalchemy.orm import relation

from vigilo.models.configure import db_basename, DeclarativeBase, DBSession
from vigilo.models.secondary_tables import SUB_MAP_NODE_MAP_TABLE

__all__ = ('MapNodeHost', 'MapNodeService', 'MapNodePerformance')

class MapNode(DeclarativeBase, object):
    """
    Classe abstraite pour représenter un nœud présent sur une carte
    affichée dans VigiMap. Les classes L{MapNodeHost}, L{MapNodeService}, etc.
    correspondent aux classes concrètes utilisées pour la représentation
    des cartes.

    @ivar idmapnode: Identifiant du modèle de nœud (séquence). 
    @ivar label: Label du nœud.
    @ivar x_pos: Abscisse du nœud.
    @ivar y_pos: Ordonnée du nœud.
    @ivar minimize: Booléen indiquant l'action à effectuer.
    @ivar type_node: Le type de nœud, peut etre
        'host', 'service',  ou 'performance'.
    @ivar idmap: Référence vers un identifiant de carte.
    @ivar map: Relation vers la carte du nœud.
    @ivar submaps: Liste des sous-cartes associées au nœud.
    """
    __tablename__ = db_basename + 'mapnode'

    idmapnode = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )
    
    label = Column(Unicode(255))

    idmap = Column(
        Integer,
        ForeignKey(
            db_basename + 'map.idmap',
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
    @ivar idhost: Identifiant de l'L{Host} représenté.
    @ivar host: Instance de l'L{Host} représenté.
    @ivar hosticon: Nom de l'icône de l'hôte. 
    @ivar hoststateicon: État de l'icône de l'hôte.
    """
    __tablename__ = 'mapnodehost'
    __mapper_args__ = {'polymorphic_identity': u'host'}
    
    idmapnode = Column(
        Integer,
        ForeignKey(
            db_basename + 'mapnode.idmapnode',
            onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        nullable=False
    )
    
    idhost = Column(
        Integer, 
        ForeignKey(
            db_basename + 'host.idhost',
            onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)

    hosticon = Column(
        Unicode(255)
        )
    
    hoststateicon = Column(
        Unicode(255)
        )
    
    host = relation('Host', lazy=True)
    
    
    def __init__(self, **kwargs):
        super(MapNodeHost, self).__init__(**kwargs)
        
        
class MapNodeService(MapNode):
    """
    Classe chargée de la représentation graphique d'un service dans VigiMap.

    @ivar idmapnode: Identifiant du modèle de service (séquence). 
    @ivar idservice: Identifiant du L{LowLevelService} représenté.
    @ivar service: Instance du L{LowLevelService} représenté.
    @ivar serviceicon: Nom de l'icône du service.
    @ivar servicestateicon: ¢tat de l'icône du service.
    """
    __tablename__ = 'mapnodeservice'
    __mapper_args__ = {'polymorphic_identity': u'service'}
    #__mapper_args__ = {'concrete':True}
    
    idmapnode = Column(
        Integer,
        ForeignKey(
            db_basename + 'mapnode.idmapnode',
            onupdate='CASCADE', ondelete='CASCADE'), 
        primary_key=True,
        nullable=False
    )

    idservice = Column(
        Integer,
        ForeignKey(
            db_basename + 'lowlevelservice.idservice',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    service = relation('LowLevelService')

    serviceicon = Column(
        Unicode(255)
        )
    
    servicestateicon = Column(
        Unicode(255)
        )

    
    def __init__(self, **kwargs):
        super(MapNodeService, self).__init__(**kwargs)

#TODO: Classe en préparation
#class MapNodePerformance(MapNode):
#    
#    Classe chargée de la représentation graphique d'un modèle Performance dans vigimap 

#    __mapper_args__ = {'polymorphic_identity': u'performance'}
#    
#    idmapnode = Column(
#        Integer,
#        ForeignKey(
#            db_basename + 'mapnode.idmapnode',
#            onupdate='CASCADE', ondelete='CASCADE'), 
#        primary_key=True,
#        nullable=False
#    )
#    
#    name = Column(
#        Unicode(255),
#        index=True, ForeignKey(db_basename + 'performance.name'),
#        ondelete='CASCADE', onupdate='CASCADE',
#        nullable=False)     
#    
#    
#    def __init__(self, **kwargs):
#        super(MapNodeService, self).__init__(**kwargs)

