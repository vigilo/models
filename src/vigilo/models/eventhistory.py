# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table EventHistory"""
from __future__ import absolute_import

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, UnicodeText, Unicode, Text, DateTime

from sqlalchemy.databases.mysql import MSEnum

from .vigilo_bdd_config import bdd_basename, DeclarativeBase

__all__ = ('EventHistory', )

class EventHistory(DeclarativeBase, object):
    """
    Cette classe enregistre un historique des modifications relatives
    à un événement (nouvelle occurrence, changement d'acquittement, etc.).

    @ivar idhistory: Identifiant de l'entrée dans l'historique.
    @ivar type_action: Le type d'action effectue, peut etre
        'Nagios update state', 'Acknowlegement change state', 'New occurence',
        'User comment', 'Ticket change', 'Oncall' ou 'Forced state'.
    @ivar idevent: Identifiant de l'événement auquel se rapporte
        cette entrée d'historique.
    @ivar event: Instance de l'événement à laquelle se rapporte l'entrée.
    @ivar value: Valeur associée a l'action. Il s'agira par exemple du
        nouvel état d'un élément supervisé, tel que transmis par Nagios.
    @ivar text: Commentaire sur l'action effectuée.
    @ivar username: Nom d'utilisateur de la personne effectuant l'action.
    """

    __tablename__ = bdd_basename + 'eventhistory'

    idhistory = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
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

    event = relation('Event', lazy=True)

    value = Column(UnicodeText)

    # On ne peut pas imposer de l'Unicode au champ "text" car son contenu
    # provient parfois de Nagios, qui n'a pas la notion d'encodages.
    text = Column(Text(length=None, convert_unicode=True, assert_unicode=None))

    timestamp = Column(DateTime(timezone=False), nullable=False)

    # Le nom d'utilisateur peut être vide dans le cas où le changement
    # est provoqué par Nagios.
    username = Column(Unicode(255))


    def __init__(self, **kwargs):
        """Initialise un événement de l'historique des modifications."""
        super(EventHistory, self).__init__(**kwargs)

