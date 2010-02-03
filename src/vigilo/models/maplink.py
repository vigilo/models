# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""
Modèle pour la table maplink et ses tables dérivées par jointure 
mapservicelink et mapsegment.
"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('Link', )

class MapLink(DeclarativeBase, object):
    """
    Informations sur une liaison dans une carte.

    @ivar idmaplink: Identifiant de la liaison.
    @ivar idfrom_node: Identifiant du nœud de départ de la liaison.
    @ivar idto_node: Identifiant du nœud d'arrivée de la liaison.
    @ivar idmap: Référence vers l'identifiant de carte de la liaison. 
    @ivar type_link: Type de liaison.
    @ivar from_node: Instance du nœud de départ de la liaison.
    @ivar to_node: Instance du nœud d'arrivée de la liaison.
    """
    __tablename__ = bdd_basename + 'maplink'

    idmaplink = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )

    idfrom_node = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'mapnode.idmapnode',
            ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    
    idto_node = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'mapnode.idmapnode',
            ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)

    idmap = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'map.idmap',
            onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    
    type_link = Column('type_link', Unicode(16), nullable=False)

    __mapper_args__ = {'polymorphic_on': type_link}

    from_node = relation('MapNode', foreign_keys=[idto_node], 
                         primaryjoin='MapLink.idto_node == MapNode.idmapnode', 
                         lazy=True)
    
    to_node = relation('MapNode', foreign_keys=[idfrom_node],
                       primaryjoin='MapLink.idfrom_node == MapNode.idmapnode',
                       lazy=True)
 
    def __init__(self, **kwargs):
        """Initialise une liaison."""
        super(MapLink, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{MapLink} pour l'afficher dans les formulaires.

        Le nom de la liaison est utilisé pour la représenter dans les formulaires.

        @return: Le nom de la liaison.
        @rtype: C{unicode}
        """
        return self.name

    @classmethod
    def by_link_name(cls, linkname):
        """
        Renvoie la liaison dont le nom est L{linkname}.
        
        @param linkname: Nom de la liaison voulue.
        @type linkname: C{unicode}
        @return: La liaison demandée.
        @rtype: L{MapLink}
        """
        return DBSession.query(cls).filter(cls.name == linkname).first()
    
    
class MapServiceLink(MapLink):
    """
    Classe chargée de la représentation graphique d'une
    liaison de type Service dans VigiMap.
    
    @ivar idmapservicelink: Identifiant du modèle de l'hôte (séquence).
    @ivar idref: Identifiant du service de bas niveau référencé.
    @ivar reference: Instance du service de bas niveau référencé.
    @ivar idgraph: Identifiant du graphe associé à la liaison.
    @ivar graph: Instance graphe associé à la liaison.
    @ivar map: Relation vers la carte.
    """
    __tablename__ = 'mapservicelink'
    __mapper_args__ = {'polymorphic_identity': u'mapservicelink'}
    
    idmapservicelink = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'maplink.idmaplink',
            onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        nullable=False
        )

    idref = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'lowlevelservice.idservice',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    reference = relation('LowLevelService')

    idgraph = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'graph.idgraph',
            ondelete='CASCADE', onupdate='CASCADE')
        )
    
    map = relation('Map',
        back_populates='links', lazy=True) 
    
        
    def __init__(self, **kwargs):
        """Initialisation d'une liaison concernant un L{LowLevelService}."""
        super(MapServiceLink, self).__init__(**kwargs)
        
        
class MapSegment(MapLink):
    """
    Classe chargée de la représentation graphique d'un segment dans VigiMap.

    @ivar idmapsegment: Identifiant du modèle de l'hôte (séquence).
    @ivar color: Couleur du segment.
    @ivar thickness: Épaisseur de trait du segment.
    @ivar map: Instance de la carte.
    """
    __tablename__ = 'mapsegment'
    __mapper_args__ = {'polymorphic_identity': u'mapsegment'}
    
    idmapsegment = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'maplink.idmaplink',
            onupdate='CASCADE', ondelete='CASCADE'),
        primary_key=True,
        nullable=False
        )
    
    color = Column(Unicode(255))
    
    thickness = Column(Integer)
    
    map = relation('Map', back_populates='segments')

