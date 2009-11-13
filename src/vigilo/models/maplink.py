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
    Informations sur une liaison de carte.
    @ivar idmaplink: Identifiant de la liaison.
    @ivar from_node: Noeud de départ de la liaison.
    @ivar to_node: Noeud d'arrivée de la liaison.
    @ivar idmap: Référence vers l'identifiant de carte de la liaison. 
    """
    __tablename__ = bdd_basename + 'maplink'

    idmaplink = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )

    from_node = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'mapnode.idmapnode',
            ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    
    to_node = Column(
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


    def __init__(self, **kwargs):
        """Initialise une liaison."""
        super(MapLink, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{MapLink} pour l'afficher dans les formulaires.

        Le nom de la liaison est utilisé pour la représenter dans les formulaires.

        @return: Le nom de la liaison.
        @rtype: C{str}
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
    Classe chargée de la représentation graphique d'une liaison Service dans vigimap
    
    @ivar idmapServicelink: Identifiant du modèle de l'hôte (séquence).
    @ivar refhost: Référence vers l'hôte associée à la liaison.
    @ivar refservice: Référence vers le service associé à la liaison.
    @ivar graph: Référence vers le graphe associé à la liaison.
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
    
    refhost = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'host.name',
            ondelete='CASCADE', onupdate='CASCADE')
        )
    
    refservice = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'service.name',
            ondelete='CASCADE', onupdate='CASCADE')
        ) 
    
    graph = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'graph.name',
            ondelete='CASCADE', onupdate='CASCADE')
        )
    
    map = relation('Map',
        back_populates='links') 
    
        
    def __init__(self, **kwargs):
        super(MapServiceLink, self).__init__(**kwargs)
        
        
class MapSegment(MapLink):
    """
    Classe chargée de la représentation graphique d'un segment dans vigimap
    Cette classe hérite de MapLink.
    @ivar idmapsegment: Identifiant du modèle de l'hôte (séquence).
    @ivar color: Couleur du segment.
    @ivar thickness: Epaisseur de trait du segment.
    @ivar map: Relation vers la carte.
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
    
    map = relation('Map',
        back_populates='segments')
