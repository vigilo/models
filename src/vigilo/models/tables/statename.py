# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table StateName"""
from sqlalchemy import Column
from sqlalchemy.types import Integer, Unicode

from vigilo.models.session import DeclarativeBase, DBSession

__all__ = ('StateName', )

class StateName(DeclarativeBase, object):
    """
    @ivar idstatename: Identifiant (auto-généré) du nom d'état.
    @ivar statename: Le nom de l'état (ex: "UP", "UNKNOWN", "OK", etc.).
    @ivar order: L'importance de l'état. Plus ce nombre est élevé,
        plus l'état a de l'importance et apparaîtra en début d'un
        tableau (cas des événements dans VigiBoard par exemple).
    """
    __tablename__ = 'statename'

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
    def __statename_mapping(cls, force_refresh):
        """
        Renvoie un dictionnaire avec les associations id <-> nom.
        Cette méthode agit comme un cache, les valeurs sont obtenues
        à la première requête qui interroge les noms d'états et mémorisées
        localement. Les requêtes suivantes utilise la valeur enregistrée
        localement sans effectuer de requêtes auprès du serveur SQL.
        """
        if not getattr(cls, '_cache', None) or force_refresh:
            values = DBSession.query(cls.idstatename, cls.statename).all()
            cls._cache = dict(values)
            cls._reversed_cache = dict([(v, k) for (k, v) in values])
        return (cls._cache, cls._reversed_cache)

    @classmethod
    def statename_to_value(cls, name):
        """Permet d'obtenir l'identifiant associé à un nom d'état donné."""
        try:
            return cls.__statename_mapping(False)[1][name]
        except KeyError:
            return cls.__statename_mapping(True)[1][name]

    @classmethod
    def value_to_statename(cls, value):
        """Permet d'obtenir le nom d'état associé à un identifiant donné."""
        try:
            return cls.__statename_mapping(False)[0][value]
        except KeyError:
            return cls.__statename_mapping(True)[0][value]

    def __init__(self, **kwargs):
        """Initialise un nom d'état."""
        super(StateName, self).__init__(**kwargs)

    def __unicode__(self):
        """Renvoie la représentation unicode du nom d'état."""
        return self.statename
