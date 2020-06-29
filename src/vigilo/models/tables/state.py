# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2020 CS GROUP – France
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table State"""
import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, Text, DateTime

from vigilo.models.session import DeclarativeBase
from vigilo.models.tables.supitem import SupItem
from vigilo.models.tables.statename import StateName

class State(DeclarativeBase, object):
    """
    Stocke un état transmis par Nagios.

    @ivar idsupitem: Identifiant de l'équipement concerné (L{SupItem}).
    @ivar supitem: Instance de l'équipement concerné (L{SupItem}).
    @ivar timestamp: Horodatage de l'état.
    @ivar state: Code de l'état dans L{vigilo.models.statename.StateName}.
    @ivar attempt: Nombre de tentatives effectuées par Nagios.
    @ivar message: Message d'état transmis par Nagios.
    """

    __tablename__ = 'vigilo_state'

    idsupitem = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        autoincrement=False,
        primary_key=True,
    )

    supitem = relation('SupItem', back_populates="state", lazy=True)

    timestamp = Column(
            DateTime(timezone=False),
            nullable=False,
            default=datetime.datetime.utcnow,
    )

    state = Column(
        'state', Integer,
        ForeignKey(
            StateName.idstatename,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )
    name = relation("StateName", uselist=False)

    attempt = Column(
        Integer,
        nullable=True,
        autoincrement=False,
    )

    # Le message stocké ici est fourni par Nagios, qui ne possède pas
    # la notion d'encodages. On tente une conversion vers Unicode,
    # mais on ne peut pas garantir le type, d'où l'utilisation du type
    # SQL générique "Text".
    message = Column(
        Text(length=None, convert_unicode=True))

    def __init__(self, **kwargs):
        """Initialise un état."""
        super(State, self).__init__(**kwargs)

    def __unicode__(self):
        return "%s [%s]" % (unicode(self.supitem), unicode(self.name))

