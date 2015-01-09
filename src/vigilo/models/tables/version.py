# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2015 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Version"""
from sqlalchemy import Column
from sqlalchemy.types import Unicode, Integer

from vigilo.models.session import DeclarativeBase, DBSession

__all__ = ('Version', )

class Version(DeclarativeBase, object):
    """
    Stocke des informations sur la version d'un composant de Vigilo.

    @ivar name: Nom du composant dont les informations de version
        sont stockées ici.
    @ivar version: Numéro de version du composant (valeur numérique
        uniquement).
    """
    __tablename__ = 'version'

    name = Column(
        Unicode(64),
        index=True,
        primary_key=True,
        nullable=False,
    )

    version = Column(
        Integer,
        nullable=False,
    )

    def __init__(self, **kwargs):
        """Initialise une instance de la classe Version."""
        super(Version, self).__init__(**kwargs)

    @classmethod
    def by_object_name(cls, object_name):
        """
        Retourne les informations de version sur le composant
        dont le nom est L{object_name}.
        
        @return: Informations de version sur le composant L{object_name}.
        @rtype: L{Version}
        """
        return DBSession.query(cls).filter(
            cls.name == unicode(object_name)).first()

