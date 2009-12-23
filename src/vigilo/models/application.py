# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Application."""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('Application', )

class Application(DeclarativeBase, object):
    """Gère les applications employées par Vigilo."""
    __tablename__ = bdd_basename + 'application'

    idapp = Column(
        Integer,
        primary_key=True, 
        autoincrement=True,
    )

    name = Column(
        Unicode(255),
        nullable=False,
        unique=True,
    )

    def __init__(self, **kwargs):
        """
        Initialise l'instance avec les informations de l'application.
        
        @param kwargs: Un dictionnaire contenant les informations sur
            l'applications.
        @type kwargs: C{dict}
        """
        super(Application, self).__init__(**kwargs)

    def __unicode__(self):
        """
        Conversion en unicode.
        
        @return: Nom du groupe d'applications.
        @rtype: C{unicode}
        """
        return self.name

    @classmethod
    def by_app_name(cls, app):
        """Renvoie une instance d'L{Application} à partir de son nom."""
        return DBSession.query(cls).filter(cls.name == app).first()

