# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2020 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table EventHistory"""
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, Unicode, Text, DateTime

from vigilo.models.utils import DateMixin
from vigilo.models.session import DeclarativeBase
from vigilo.models.tables.event import Event
from vigilo.models.tables.statename import StateName

__all__ = ('EventHistory', )

class EventHistory(DeclarativeBase, DateMixin):
    """
    Cette classe enregistre un historique des modifications relatives
    à un événement (nouvelle occurrence, changement d'acquittement, etc.).

    @ivar idhistory: Identifiant de l'entrée dans l'historique.
    @ivar type_action: Le type d'action effectué, peut être :
        - 'New occurence' : Création d'un évènement
            corrélé à la réception d'une alerte Nagios ;
        - 'Nagios update state' : Mise à jour de l'état
            de l'item et de l'évènement corrélé suite
            à la réception d'une alerte Nagios ;
        - 'Acknowlegement change state' : Remise à zéro de
            l'état d'un évènement corrélé acquitté par l'opérateur
            alors que Nagios continue à envoyer des alertes ;
        - 'Ticket change' : Changement du ticket d'incident par l'opérateur ;
        - 'Ticket change notification' : Réception d'une
            notification de la modification d'un ticket d'incident ;
        - 'User comment' : plus utilisé ? ;
        - 'Oncall' : plus utilisé ? ;
        - 'Forced state' : plus utilisé ?.
    @ivar idevent: Identifiant de l'événement auquel se rapporte
        cette entrée d'historique.
    @ivar event: Instance de l'événement à laquelle se rapporte l'entrée.
    @ivar value: Valeur associée a l'action. Il s'agira par exemple du
        nouvel état d'un élément supervisé, tel que transmis par Nagios.
    @ivar text: Commentaire sur l'action effectuée.
    @ivar timestamp: Date à laquelle le changement a eu lieu.
    @ivar username: Nom d'utilisateur de la personne effectuant l'action.

    @note: Cette classe permet de répondre aux exigences suivantes :
        VIGILO_EXIG_VIGILO_BAC_0020.
    """

    __tablename__ = 'vigilo_eventhistory'

    idhistory = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    type_action = Column(Unicode(64), nullable=False, index=True)

    idevent = Column(
        Integer,
        ForeignKey(
            Event.idevent,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        index=True,
        nullable=False,
        autoincrement=False,
    )

    event = relation('Event', lazy=True)

    value = Column(Unicode(255))

    # On ne peut pas imposer de l'Unicode au champ "text" car son contenu
    # provient parfois de Nagios, qui n'a pas la notion d'encodages.
    text = Column(Text(length=None, convert_unicode=True))

    timestamp = Column(DateTime(timezone=False), nullable=False)

    # Le nom d'utilisateur peut être vide dans le cas où le changement
    # est provoqué par Nagios.
    username = Column(Unicode(255))

    state = Column(
        Integer,
        ForeignKey(
            StateName.idstatename,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=True,
        autoincrement=False,
    )


    def __init__(self, **kwargs):
        """Initialise un événement de l'historique des modifications."""
        super(EventHistory, self).__init__(**kwargs)

