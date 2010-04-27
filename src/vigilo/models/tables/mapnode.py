# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
Modèle pour la table MapNode
"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, Boolean
from sqlalchemy.orm import relation

from vigilo.models.session import DeclarativeBase, ForeignKey
from vigilo.models.tables.secondary_tables import SUB_MAP_NODE_MAP_TABLE
from vigilo.models.tables.map import Map
from vigilo.models.tables.host import Host
from vigilo.models.tables.service import Service

__all__ = ('MapNodeHost', 'MapNodeService', 'MapNodeLls', 'MapNodeHls', 
           'MapNodePerformance')

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
    @ivar icon: Nom de l'icône du noeud.
    @ivar map: Relation vers la carte du nœud.
    @ivar submaps: Liste des sous-cartes associées au nœud.
    """
    __tablename__ = 'mapnode'

    idmapnode = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )
    
    label = Column(Unicode(255))

    idmap = Column(
        Integer,
        ForeignKey(
            Map.idmap,
            onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    
    x_pos = Column(Integer, nullable=True)
    
    y_pos = Column(Integer, nullable=True)
    
    minimize = Column(
        Boolean, 
        default = False,
        nullable = False)

    widget = Column(Unicode(32), nullable=False, default=u"SimpleElement")

    map = relation('Map', back_populates='nodes')
    
    submaps = relation('Map', secondary=SUB_MAP_NODE_MAP_TABLE)
    
    type_node = Column('type_node', Unicode(16))
    
    icon = Column(
        Unicode(255)
        )
    
    links_from = relation('MapLink', foreign_keys=[idmapnode],
                    primaryjoin='MapLink.idfrom_node == ' + \
                        'MapNode.idmapnode')
    
    links_to = relation('MapLink', foreign_keys=[idmapnode],
                    primaryjoin='MapLink.idto_node == ' + \
                        'MapNode.idmapnode')

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

    @classmethod
    def by_map_label(cls, idmap, label):
        if not isinstance(idmap, int):
            idmap = idmap.idmap
        return DBSession.query(cls).filter(
                    cls.idmap == idmap
                ).filter(
                    cls.label == label
                ).first()


class MapNodeHost(MapNode):
    """
    Classe chargée de la représentation graphique d'un hôte dans vigimap
    
    @ivar idmapnode: Identifiant du modèle de l'hôte (séquence). 
    @ivar idhost: Identifiant de l'L{Host} représenté.
    @ivar host: Instance de l'L{Host} représenté.
    """
    __tablename__ = 'mapnodehost'
    __mapper_args__ = {'polymorphic_identity': u'host'}
    
    idmapnode = Column(
        Integer,
        ForeignKey(
            MapNode.idmapnode,
            onupdate='CASCADE', ondelete='CASCADE'),
        autoincrement=True, primary_key=True,
        nullable=False
    )
    
    idhost = Column(
        Integer, 
        ForeignKey(
            Host.idhost,
            onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False)
    
    host = relation('Host', lazy=True)
    
    
    def __init__(self, **kwargs):
        super(MapNodeHost, self).__init__(**kwargs)
        
        
class MapNodeService(MapNode):
    """
    Classe chargée de la représentation graphique d'un service dans VigiMap.

    @ivar idmapnode: Identifiant du modèle de service (séquence). 
    @ivar idservice: Identifiant du L{Service} représenté.
    @ivar service: Instance du L{Service} représenté.
     """
    __tablename__ = 'mapnodeservice'
    
    idmapnode = Column(
        Integer,
        ForeignKey(
            MapNode.idmapnode,
            onupdate='CASCADE', ondelete='CASCADE'), 
        autoincrement=False, primary_key=True,
        nullable=False
    )

    idservice = Column(
        Integer,
        ForeignKey(
            Service.idservice,
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    service = relation('Service')

    
    def __init__(self, **kwargs):
        super(MapNodeService, self).__init__(**kwargs)


class MapNodeLls(MapNodeService):
    """
    Classe chargée de la représentation graphique d'un service de bas niveau
    dans VigiMap.
 
    """
    
    __mapper_args__ = {'polymorphic_identity': u'lls'}
    
    
    
class MapNodeHls(MapNodeService):
    """
    Classe chargée de la représentation graphique d'un service de haut niveau
    dans VigiMap.

    """

    __mapper_args__ = {'polymorphic_identity': u'hls'}
    

#TODO: Classe en préparation
#class MapNodePerformance(MapNode):
#    
#    Classe chargée de la représentation graphique d'un modèle
#    Performance dans vigimap 

#    __mapper_args__ = {'polymorphic_identity': u'performance'}
#    
#    idmapnode = Column(
#        Integer,
#        ForeignKey(
#            'mapnode.idmapnode',
#            onupdate='CASCADE', ondelete='CASCADE'), 
#        primary_key=True,
#        nullable=False
#    )
#    
#    name = Column(
#        Unicode(255),
#        index=True, ForeignKey('performance.name'),
#        ondelete='CASCADE', onupdate='CASCADE',
#        nullable=False)     
#    
#    
#    def __init__(self, **kwargs):
#        super(MapNodeService, self).__init__(**kwargs)

