# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table EventHistory"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, UnicodeText, Unicode, Text, DateTime

from sqlalchemy.databases.mysql import MSEnum

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('EventHistory', )

class EventHistory(DeclarativeBase, object):
    """
    @ivar type_action: Le type d'action effectue, peut etre
        'Nagios update state', 'Acknowlegement change state', 'New occurence',
        'User comment', 'Ticket change', 'Oncall' ou 'Forced state'.
    @ivar idevent: Identifiant de l'evenement.
    @ivar value: Valeur associee a l'action.
    @ivar text: Commentaire sur l'action effectuee.
    @ivar username: Nom d'utilisateur de la personne effectuant l'action.
    """

    __tablename__ = bdd_basename + 'eventhistory'

    idhistory = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True,
    )

    type_action = Column(
        MSEnum('Nagios update state', 'Acknowlegement change state',
            'New occurence', 'User comment', 'Ticket change', 'Oncall',
            'Forced state'),
        nullable=False,
    )

    idevent = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'event.idevent'
        ),
        index=True, nullable=False, autoincrement=False,
    )

    value = Column(UnicodeText)

    text = Column(Text(length=None, convert_unicode=True, assert_unicode=None))

    timestamp = Column(DateTime(timezone=False), nullable=False)

    username = Column(Unicode(255))


    def __init__(self, **kwargs):
        """Initialise un événement de l'historique des modifications."""
        super(EventHistory, self).__init__(**kwargs)

