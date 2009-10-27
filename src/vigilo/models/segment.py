# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Segment"""
from __future__ import absolute_import

from sqlalchemy import Column,ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .secondary_tables import SEGMENT_NODE_TABLE

__all__ = ('Link', )

class Segment(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'segment'
    
    idsegment = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )

    name = Column(
        Unicode(255),
        index=True, nullable=False)

    color = Column(
        Unicode(255),
        nullable=False)
    
    thickness = Column(Integer)
    
    mapadress = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'map.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    
    nodemaps = relation('NodeMap', secondary=SEGMENT_NODE_TABLE, back_populates='segments', uselist=True )
    
    maps = relation('Map', back_populates='segments')


    def __init__(self, **kwargs):
        """Initialise une liaison."""
        super(Link, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Link} pour l'afficher dans les formulaires.

        Le nom de la liaison est utilisé pour la représenter dans les formulaires.

        @return: Le nom de la liaison.
        @rtype: C{str}
        """
        return self.name

    @classmethod
    def by_link_name(cls, linkname):
        """
        Renvoie l'hôte dont le nom est L{linkname}.
        
        @param linkname: Nom de la liasion voulue.
        @type linkname: C{unicode}
        @return: La liaison demandée.
        @rtype: L{Link}
        """
        return DBSession.query(cls).filter(cls.name == linkname).first()

