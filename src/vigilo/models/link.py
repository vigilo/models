# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Link"""
from __future__ import absolute_import

from sqlalchemy import Column,ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
#from .secondary_tables import MAP_LINK_TABLE

__all__ = ('Link', )

class Link(DeclarativeBase, object):
    __tablename__ = bdd_basename + 'link'

    idlink = Column(
        Integer,
        primary_key=True, autoincrement=True, nullable=False,
    )

    from_node = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'nodemap.idnodemap',
            ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)
    
    to_node = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'nodemap.idnodemap',
            ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False)

    x_pos = Column(Integer)
    
    y_pos = Column(Integer)    
    
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
    
    mapadress = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'map.name',
            onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)

    maps = relation('Map',
        back_populates='links')
    
    #, secondary=MAP_LINK_TABLE, lazy='dynamic'


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

