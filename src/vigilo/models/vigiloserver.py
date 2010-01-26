# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""VigiloServer model"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.orm import relation

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('VigiloServer', )

class VigiloServer(DeclarativeBase, object):
    """
    Vigilo server class.

    @ivar name: Nom complet (FQDN) du serveur.
    @ivar description: Une description intelligible du serveur.
    @ivar hostgroups: Liste des groupes d'hôtes auxquels cet hôte appartient.
    @ivar tags: Liste des libellés attachés à cet hôte.
    """
    __tablename__ = bdd_basename + 'vigiloserver'
    
    
    idvigiloserver = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    
    name = Column(
        Unicode(255),
        index=True,
        unique=True,
        nullable=False,
    )
    
    description = Column(
        UnicodeText,
        nullable=True,
    )

    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations du serveur.
        
        @param kwargs: Un dictionnaire avec les informations.
        @type kwargs: C{dict}
        """
        super(VigiloServer, self).__init__(**kwargs)
    
    def __unicode__(self):
        """
        Conversion en unicode.
        
        @return: Le nom du groupe.
        @rtype: C{str}
        """
        return self.name
    
    
    @classmethod
    def by_vigiloserver_name(cls, vigiloserver):
        """
        Renvoie le serveur dont le nom est C{vigiloservername}.

        @param cls: La classe à utiliser, c'est-à-dire L{VigiloServer}.
        @type cls: C{class}
        @param vigiloserver: Le nom du groupe que l'on souhaite récupérer.
        @type vigiloserver: C{str}
        @return: Le serveur demandé.
        @rtype: Une instance de la classe L{VigiloServer}
        """
        return DBSession.query(cls).filter(cls.name == vigiloserver).first()

