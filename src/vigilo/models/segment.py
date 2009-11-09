# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Segment"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .secondary_tables import SEGMENT_NODE_TABLE

__all__ = ('Segment', )

class Segment(DeclarativeBase, object):
    """
    Informations sur un segment de carte.
    @ivar idsegment: Identifiant du segment.
    @ivar color: Couleur du segment.
    @ivar thickness: Epaisseur de trait du segment.
    @ivar idmap: Référence vers l'identifiant de la carte associée.
    @ivar nodes: Liste des noeuds associés au segment.
    @ivar maps: Relation vers la carte associée au segment.
    """
    __tablename__ = bdd_basename + 'segment'
    
    idsegment = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )

    color = Column(
        Unicode(255),
        nullable=False)
    
    thickness = Column(Integer)
    
    idmap = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'map.idmap',
            onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    
    nodes = relation('MapNode', secondary=SEGMENT_NODE_TABLE, back_populates='segments', uselist=True)
    
    maps = relation('Map', back_populates='segments')


    def __init__(self, **kwargs):
        """Initialise une liaison."""
        super(Segment, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Formatte un C{Segment} pour l'afficher dans les formulaires.

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
        @rtype: L{Segment}
        """
        return DBSession.query(cls).filter(cls.name == linkname).first()

