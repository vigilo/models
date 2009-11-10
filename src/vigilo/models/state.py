# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table State"""

from __future__ import absolute_import

import datetime

from sqlalchemy import Column, DefaultClause, ForeignKey
from sqlalchemy.orm import synonym, interfaces, ComparableProperty, composite
from sqlalchemy.types import Integer, Text, DateTime, Unicode
from sqlalchemy.sql.expression import literal_column

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

class State(DeclarativeBase, object):
    """
    Stocke un état transmis par Nagios.

    @ivar idstate: Identifiant de l'état, autogénéré.
    @ivar hostname: Nom de l'hôte concerné. Vaut None pour les services
        de haut niveau.
    @ivar servicename: Nom du service concerné. Vaut None lorsque l'état
        concerne directement l'hôte.
    @ivar ip: Adresse IP (v4 ou v6) de l'hôte.
    @ivar timestamp: Horodattage de l'état.
    @ivar statename: Valeur de l'état (OK, WARNING, UP, DOWN, etc.)
        sous forme textuelle.
    @ivar statetype: Type d'état (cf. Nagios). Vaut soit 'SOFT', soit 'HARD'.
    @ivar attempt: Nombre de tentatives effectuées par Nagios.
    @ivar message: Message d'état transmis par Nagios.
    """

    __tablename__ = bdd_basename + 'state'

    idstate = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True)

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename +'host.name'),
        index=True, nullable=True,
    )

    servicename = Column(
        Unicode(255),
        ForeignKey(bdd_basename + 'service.name'),
        index=True, nullable=True,
    )

    ip = Column(
        Unicode(40),    # 39 caractères sont requis pour stocker une IPv6
                        # sous forme canonique. On arrondit à 40 caractères.
        nullable=True,
    )

    timestamp = Column(
            DateTime(timezone=False),
            nullable=False,
            default=datetime.datetime.now,
    )

    statename = Column(
        'state', Unicode(16),
        nullable=False, index=True,
    )

    # 'SOFT' ou 'HARD'
    statetype = Column(
        Unicode(8),
        nullable=False,
        default=u"SOFT",
    )

    attempt = Column(
        Integer,
        nullable=True,
        autoincrement=False,
    )

    message = Column(
        Text(length=None, convert_unicode=True, assert_unicode=None))

    @staticmethod
    def _names_mapping():
        """
        Définit une relation entre le nom de l'état dans Nagios
        et une valeur numérique stockée en base de données.
        """
        return [
            'OK',           # 0
            'UNKNOWN',
            'WARNING',
            'CRITICAL',

            'UP',           # 4
            'DOWN',
            'UNREACHABLE',
        ]

    @classmethod
    def statename_to_value(cls, name):
        return cls._names_mapping().index(name.upper())

    @classmethod
    def value_to_statename(cls, value):
        return cls._names_mapping()[value]

    def __init__(self, **kwargs):
        """Initialise un état."""
        super(State, self).__init__(**kwargs)

