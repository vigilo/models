# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Map"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Unicode, DateTime, Integer
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
#from .secondary_tables import MAP_LINK_TABLE, MAP_GROUP_PERMISSION_TABLE
from .secondary_tables import MAP_GROUP_MAP_TABLE

__all__ = ('Map', )

class Map(DeclarativeBase, object):
    """
    @ivar idmap: Identifiant de la carte.
    @ivar title: Titre de la carte.
    @ivar background_color: Couleur d'arrière-plan 
        (valeur de la propriété CSS background-color).
    @ivar background_image: Image d'arrière-plan (propriété CSS).
    @ivar background_position: Position d'arrière-plan (propriété CSS).
    @ivar background_repeat: Répétition d'arrière-plan (propriété CSS). 
    """
    __tablename__ = bdd_basename + 'map'

    idmap = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    
    mtime = Column(DateTime(timezone=False))
    
    title = Column(Unicode(255), nullable=False)
    
    background_color = Column(Unicode(255))
    background_image = Column(Unicode(255))
    background_position = Column(Unicode(255))
    background_repeat = Column(Unicode(255))
    
    """nodeforsubmap = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'mapnode.idmapnode'),
        nullable=True)
    """
    
    groups = relation('MapGroup', secondary=MAP_GROUP_MAP_TABLE,
                         back_populates='maps', lazy='dynamic')

    links = relation('Link', back_populates='maps', uselist=True)
    #, secondary=MAP_LINK_TABLE, lazy='dynamic'
    
    nodes = relation('MapNode', back_populates='map', uselist=True)
    
    segments = relation('Segment', back_populates='maps', uselist=True)


    def __init__(self, **kwargs):
        """Initialise une carte."""
        super(Map, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Map} pour l'afficher dans les formulaires.

        Le nom de la carte est utilisé pour le représenter dans les formulaires.

        @return: Le nom de la carte.
        @rtype: C{str}
        """
        return self.name

    @classmethod
    def by_map_name(cls, mapname):
        """
        Renvoie la carte dont le nom est L{mapname}.
        
        @param mapname: Nom de la carte voulue.
        @type mapname: C{unicode}
        @return: La carte demandée.
        @rtype: L{Map}
        """
        return DBSession.query(cls).filter(cls.name == mapname).first()

