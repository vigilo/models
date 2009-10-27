# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Map"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode, UnicodeText, DateTime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation
from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
#from .secondary_tables import MAP_LINK_TABLE
from .secondary_tables import MAP_GROUP_PERMISSION_TABLE, MAP_GROUP_MAP_TABLE

__all__ = ('Map', )

class Map(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'map'

    name = Column(
        Unicode(255),
        index=True, primary_key=True, 
        nullable=False)
    
    dat = Column(DateTime(timezone=False))

    mapgroups = relation('MapGroup', secondary=MAP_GROUP_MAP_TABLE, back_populates='maps', lazy='dynamic')

    links = relation('Link',
        back_populates='maps', uselist=True)
    #, secondary=MAP_LINK_TABLE, lazy='dynamic'
    
    nodes = relation('NodeMap', back_populates='maps', 
                    uselist=True)
    
    segments = relation('Segment',
        back_populates='maps', uselist=True)

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

