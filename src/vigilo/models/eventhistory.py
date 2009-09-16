# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table EventHistory"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.types import Integer, UnicodeText, Unicode, Text, DateTime

from sqlalchemy.databases.mysql import MSEnum
from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('EventHistory', )

class EventHistory(DeclarativeBase, object):
    """
    @param type_action: Le type d'action effectué, peut être 'Nagios update state',
                        'Acknowlegement change state', 'New occurence', 'User comment', 'Ticket change',
                        'Oncall' ou 'Forced state'
    @param idevent: Identifiant de l'évènement
    @param value: Nouvelle sévérité
    @param text: Commentaire sur l'action effectuée
    @param username: Nom d'utilisateur de la personne effectuant l'action
    """

    __tablename__ = bdd_basename + 'event_history'

    idhistory = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True)

    type_action = Column(
        MSEnum('Nagios update state', 'Acknowlegement change state',
            'New occurence', 'User comment', 'Ticket change', 'Oncall',
            'Forced state'),
        nullable=False)

    idevent = Column(
        Unicode(255),
        ForeignKey(
            bdd_basename + 'event.idevent'
        ),
        index=True, nullable=False)

    value = Column(UnicodeText)

    text = Column(Text(length=None, convert_unicode=True, assert_unicode=None))

    timestamp = Column(DateTime(timezone=False), default=datetime.now())

    username = Column(Unicode(255))


    def __init__(self, **kwargs):
        """Initialise un évènement de l'historique des modifications."""
        DeclarativeBase.__init__(self, **kwargs)

