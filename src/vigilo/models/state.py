# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table State"""

from __future__ import absolute_import

import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, Text, DateTime, Unicode

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

    _idstate = Column(
        'idstate', Integer,
        primary_key=True, autoincrement=True,
    )

    timestamp = Column(
            DateTime(timezone=False),
            nullable=False,
            default=datetime.datetime.now,
    )

    state = Column(
        'state', Integer,
        ForeignKey(
            bdd_basename + 'statename.idstatename',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        nullable=False,
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

    _statetable = Column(
        'statetable', Unicode(8),
        index=True, nullable=False,
    )

    __mapper_args__ = {'polymorphic_on': _statetable}

    def __init__(self, **kwargs):
        """Initialise un état."""
        super(State, self).__init__(**kwargs)

class HostState(State):
    __tablename__ = bdd_basename + 'hoststate'
    __mapper_args__ = {'polymorphic_identity': u'host'}

    _idstate = Column(
        'idstate', Integer,
        ForeignKey(
            bdd_basename + 'state.idstate',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True, autoincrement=True,
    )

    _hostname = Column(
        'hostname', Unicode(255),
        ForeignKey(
            bdd_basename + 'host.name',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        unique=True, index=True,
    )

    host = relation('Host')

class ServiceState(State):
    __tablename__ = bdd_basename + 'servicestate'
    __mapper_args__ = {'polymorphic_identity': u'service'}

    _idstate = Column(
        'idstate', Integer,
        ForeignKey(
            bdd_basename + 'state.idstate',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        primary_key=True, autoincrement=True,
    )

    _idservice = Column(
        'idservice', Integer,
        ForeignKey(
            bdd_basename + 'service.idservice',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        unique=True, autoincrement=False,
    )

    service = relation('Service')

