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

    @ivar idsupitem: Identifiant de l'équipement concerné.
    @ivar timestamp: Horodattage de l'état.
    @ivar state: Code de l'état dans L{vigilo.models.statename.StateName}.
    @ivar attempt: Nombre de tentatives effectuées par Nagios.
    @ivar message: Message d'état transmis par Nagios.
    """

    __tablename__ = bdd_basename + 'state'

    idsupitem = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'supitem.idsupitem',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        autoincrement=False, primary_key=True,
    )

    supitem = relation('SupItem')

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

    attempt = Column(
        Integer,
        nullable=True,
        autoincrement=False,
    )

    message = Column(
        Text(length=None, convert_unicode=True, assert_unicode=None))

    def __init__(self, **kwargs):
        """Initialise un état."""
        super(State, self).__init__(**kwargs)

