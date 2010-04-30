# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Map"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, DateTime, Integer, Boolean
from sqlalchemy.orm import relation, aliased

from vigilo.models.session import DeclarativeBase, DBSession
from vigilo.models.tables.secondary_tables import MAP_GROUP_TABLE, \
                        MAP_PERMISSION_TABLE, SUB_MAP_NODE_MAP_TABLE

__all__ = ('Map', )

class Map(DeclarativeBase, object):
    """
    Informations sur une carte.
    @ivar idmap: Identifiant de la carte.
    @ivar mtime: Date de dernière modification de la carte.
    @ivar title: Titre de la carte.
    @ivar background_color: Couleur d'arrière-plan (propriété CSS).
    @ivar background_image: Image d'arrière-plan (propriété CSS).
    @ivar background_position: Position d'arrière-plan (propriété CSS).
    @ivar background_repeat: Répétition d'arrière-plan (propriété CSS). 
    @ivar groups: Liste des L{MapGroup}s auxquels cette carte appartient.
    @ivar links: Liste des liaisons (L{MapServiceLink}) présentes sur la carte.
    @ivar nodes: Liste des nœuds (L{MapNode}) présents sur la carte.
    @ivar segments: Liste des segments (L{MapSegment}) présents sur la carte.
    @ivar permissions: Liste des L{Permission}s donnant accès à la carte.
    """
    __tablename__ = 'map'

    idmap = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    
    mtime = Column(DateTime(timezone=False))
    
    title = Column(Unicode(255), nullable=False)
    
    background_color = Column(Unicode(8))
    background_image = Column(Unicode(255))
    background_position = Column(Unicode(255))
    background_repeat = Column(Unicode(255))
    generated =  Column(
        Boolean, 
        default = False,
        nullable = False)
    
    groups = relation('MapGroup', secondary=MAP_GROUP_TABLE,
                         back_populates='maps', lazy=True)

    links = relation('MapServiceLink', back_populates='map', lazy=True)
    
    nodes = relation('MapNode', back_populates='map', lazy=True)
    
    segments = relation('MapSegment', back_populates='map', lazy=True)
    
    permissions = relation('Permission', secondary=MAP_PERMISSION_TABLE,
                            back_populates='maps', lazy=True)


    def __init__(self, **kwargs):
        """Initialise une carte."""
        super(Map, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Map} pour l'afficher dans les formulaires.

        Le titre de la carte est utilisé pour représenter la carte
        dans les formulaires.

        @return: Le titre de la carte.
        @rtype: C{unicode}
        """
        return self.title

    @classmethod
    def by_map_title(cls, maptitle):
        """
        Renvoie la carte dont le titre est L{maptitle}.
        
        @param maptitle: Titre de la carte voulue.
        @type maptitle: C{unicode}
        @return: L'instance correspondant à la carte demandée.
        @rtype: L{Map}
        """
        return DBSession.query(cls).filter(cls.title == maptitle).first()

    @classmethod
    def has_submaps(cls, idmap):
        from .mapnode import MapNode
        MAlias = aliased(Map)
        return (DBSession.query(MAlias)\
            .join((SUB_MAP_NODE_MAP_TABLE, 
                   SUB_MAP_NODE_MAP_TABLE.c.idmap == MAlias.idmap))\
            .join((MapNode, 
                   MapNode.idmapnode == SUB_MAP_NODE_MAP_TABLE.c.mapnodeid))\
            .join((cls, cls.idmap == MapNode.idmap))\
            .filter(cls.idmap == idmap)\
            .count() > 0)

    @classmethod
    def get_submaps(cls, idmap):
        from .mapnode import MapNode
        MAlias = aliased(Map)
        return (DBSession.query(MAlias)\
            .join((SUB_MAP_NODE_MAP_TABLE, 
                   SUB_MAP_NODE_MAP_TABLE.c.idmap == MAlias.idmap))\
            .join((MapNode, 
                   MapNode.idmapnode == SUB_MAP_NODE_MAP_TABLE.c.mapnodeid))\
            .join((cls, cls.idmap == MapNode.idmap))\
            .filter(cls.idmap == idmap).distinct().order_by(Map.title).all())
                   
            