# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table State"""

from __future__ import absolute_import

import datetime

from sqlalchemy import Column, DefaultClause, ForeignKey
from sqlalchemy.orm import synonym
from sqlalchemy.orm import interfaces
from sqlalchemy.ext.declarative import comparable_property
from sqlalchemy.types import Integer, Text, DateTime, Unicode

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

def state_proxy(num_state):
    """
    Permet de lier entre elles la représentation textuelle
    et la représentation numérique d'un état.

    Cette fonction est à utiliser dans une classe dérivée de
    DeclarativeBase, de la manière suivante :

    numeric_current_state = Column(
        'current_state', Integer,
        autoincrement=False, nullable=False,
    )
    state = state_proxy('numeric_current_state')

    @param num_state: Le nom de l'attribut dans la classe contenant
        la représentation numérique de l'état.
    @type num_state: C{str}
    @return: Un attribut utilisable avec les mécanismes de SQLAlchemy.
    @rtype: C{SynonymProperty}
    """

    def getter(self):
        """Renvoie la valeur textuelle de l'état."""
        return State.names_mapping()[self.__getattribute__(num_state)]

    def setter(self, value):
        """
        Modifié la valeur de l'état à partir de sa
        représentation textuelle.
        """
        self.__setattr__(num_state,
            State.names_mapping().index(value.upper()))

    class Comparator(interfaces.PropComparator):
        """Comparateur entre 2 valeurs textuelles d'un état."""
        def __eq__(self, other):
            """Opération de comparaison."""
            return self.mapper.class_.__getattribute__(
                self.mapper.class_, num_state) == \
                State.names_mapping().index(other.upper())

    attribute = synonym(num_state, descriptor=property(getter, setter))
    attribute = comparable_property(Comparator, attribute.descriptor)
    return attribute


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
    @ivar numeric_state: Valeur de l'état (OK, WARNING, UP, DOWN, etc.)
        sous forme numérique.
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

    numeric_state = Column(
        'state', Integer,
        nullable=False, autoincrement=False,
    )
    statename = state_proxy('numeric_state')

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
    def names_mapping():
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

    def __init__(self, **kwargs):
        """Intiialise un état."""
        super(State, self).__init__(**kwargs)

