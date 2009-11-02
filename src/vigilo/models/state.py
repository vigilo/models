# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table State"""

from __future__ import absolute_import

import datetime

from sqlalchemy import Column, DefaultClause, ForeignKey
from sqlalchemy.orm import synonym, interfaces
from sqlalchemy.ext.declarative import comparable_property
from sqlalchemy.types import Integer, Text, DateTime, Unicode

from .vigilo_bdd_config import bdd_basename, DeclarativeBase


class State(DeclarativeBase, object):

    __tablename__ = bdd_basename + 'state'

    idstate = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True)

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename +'host.name'),
        index=True, nullable=False)

    servicename = Column(
        Unicode(255),
        ForeignKey(bdd_basename + 'service.name'),
        index=True)

    ip = Column(
        Unicode(40),    # 39 caractères sont requis pour stocker une IPv6
                        # sous forme canonique. On arrondit à 40 caractères.
    )

    timestamp = Column(
            DateTime(timezone=False),
            nullable=False,
            default=datetime.datetime.now,
    )

    statename = Column(
        Unicode(16),
        nullable=False,
        default=u"OK",
    )

    # 'SOFT' ou 'HARD'
    statetype = Column(
        Unicode(8),
        nullable=False,
        default=u"SOFT",
    )

    attempt = Column(
        Integer,
        nullable=False,
        autoincrement=False,
        default=1,
    )

    message = Column(
        Text(length=None, convert_unicode=True, assert_unicode=None))

    @staticmethod
    def names_mapping():
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


def state_proxy(num_state, text_state):
    """
    Permet de lier entre elles la représentation textuelle
    et la représentation numérique d'un état.

    Cette fonction est à utiliser dans une classe dérivée de
    DeclarativeBase, de la manière suivante :

    numeric_current_state = Column(
        'current_state', Integer,
        autoincrement=False, nullable=False,
    )
    state = state_proxy('numeric_current_state', 'state')

    @param num_state: Le nom de l'attribut dans la classe contenant
        la représentation numérique de l'état.
    @type num_state: C{str}
    @param text_state: Le nom de l'attribut dans la classe contentant
        la représentation textuelle de l'état. Il s'agira généralement
        du nom de la variable dans laquelle la valeur de retour de cette
        fonction sera stockée.
    @type text_state: C{str}
    @return: Un attribut utilisable avec les mécanismes de SQLAlchemy.
    @rtype: C{SynonymProperty}
    """

    def getter(self):
        return State.names_mapping()[self.__getattribute__(num_state)]

    def setter(self, value):
        self.__setattr__(num_state,
            State.names_mapping().index(value.upper()))

#    class comparator(interfaces.PropComparator):
#        def __eq__(self, other):
#            return self.__getattr__(num_state) == \
#                other.__getattr__(num_state)

    attribute = synonym(num_state, descriptor=property(getter, setter))
#    attribute = comparable_property(comparator, attribute.descriptor)
    return attribute

