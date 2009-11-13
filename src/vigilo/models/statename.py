# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Statename"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('Statename', )

class Statename(DeclarativeBase, object):
    """
    @ivar idstatename: Identifiant (auto-généré) de la classe.
    @ivar statename: Le nom de l'état (ex: "UP", "UNKNOWN", "OK", etc.).
    @ivar order: L'importance de l'état.
    """
    __tablename__ = bdd_basename + 'statename'

    idstatename = Column(
        Integer,
        primary_key=True, autoincrement=True,
    )

    statename = Column(
        Unicode(16),
        unique=True, index=True,
        nullable=False,
    )

    order = Column(
        Integer,
        nullable=False,
    )

    @classmethod
    def __statename_mapping(cls):
        def inner():
            query =   DBSession.query(
                            cls.idstatename,
                            cls.statename,
                        )
            # TODO: est-ce que ca marche si les cles primaires ne commencent pas a 1 ? J'en doute
            mapping = list(dict(query.all()).values())
            mapping.insert(0, None)

            while True:
                yield mapping
        return inner().next

    @classmethod
    def statename_to_value(cls, name):
        return cls.__statename_mapping()().index(name.upper())

    @classmethod
    def value_to_statename(cls, value):
        return cls.__statename_mapping()()[value]

    def __init__(self, **kwargs):
        """Initialise un nom d'état."""
        super(Statename, self).__init__(**kwargs)

    def __unicode__(self):
        """Renvoie la représentation unicode du nom d'état."""
        return self.statename

