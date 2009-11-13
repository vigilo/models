# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table StateName"""
from __future__ import absolute_import

from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession

__all__ = ('StateName', )

class StateName(DeclarativeBase, object):
    """
    @ivar idstatename: Identifiant (auto-généré) de la classe.
    @ivar statename: Le nom de l'état (ex: "UP", "UNKNOWN", "OK", etc.).
    @ivar order: L'importance de l'état. Plus ce nombre est élevé,
        plus l'état a d'importance et devrait apapraître en premier
        dans un tableau par exemple.
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
        """Renvoie un dictionnaire avec les associations id <-> nom."""
        def inner():
            """Renvoie un itérateur sur le dictionnaire des associations."""
            query =   DBSession.query(
                            cls.idstatename,
                            cls.statename,
                        )
            mapping = dict(query.all())
            while True:
                yield mapping
        return inner().next

    @classmethod
    def statename_to_value(cls, name):
        """Permet d'obtenir l'identifiant associé à un nom d'état donné."""
        mapping = cls.__statename_mapping()()
        for k in mapping:
            if mapping[k] == name:
                return k
        raise KeyError, ("No such statename '%s'" % name)

    @classmethod
    def value_to_statename(cls, value):
        """Permet d'obtenir le nom d'état associé à un identifiant donné."""
        return cls.__statename_mapping()()[value]

    def __init__(self, **kwargs):
        """Initialise un nom d'état."""
        super(StateName, self).__init__(**kwargs)

    def __unicode__(self):
        """Renvoie la représentation unicode du nom d'état."""
        return self.statename

