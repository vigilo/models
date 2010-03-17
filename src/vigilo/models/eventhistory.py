# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table EventHistory"""
from sqlalchemy import Column
from sqlalchemy.orm import relation
from sqlalchemy.types import Integer, UnicodeText, Unicode, Text, DateTime

from datetime import datetime

from sqlalchemy.databases.mysql import MSEnum

from vigilo.models.configure import DeclarativeBase, ForeignKey
from vigilo.models.event import Event

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
    @ivar timestamp: Date à laquelle le changement a eu lieu.
    @ivar username: Nom d'utilisateur de la personne effectuant l'action.
    """

    __tablename__ = 'eventhistory'

    idhistory = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )

    type_action = Column(
        MSEnum('Nagios update state', 'Acknowledgement change state',
            'New occurence', 'User comment', 'Ticket change',
            'Ticket change notification', 'Oncall', 'Forced state'),
        nullable=False,
    )

    idevent = Column(
        Integer,
        ForeignKey(Event.idevent),
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

    def get_date(self, element):
        """
        Permet de convertir une variable de temps en la chaîne de caractère :
        jour mois heure:minutes:secondes

        @param element: nom de l'élément à convertir de la classe elle même
        @type element: C{unicode}
        @return: La date demandée.
        @rtype: C{unicode}
        """

        element = getattr(self, element)
        date = datetime.now() - element
        if date.days < 7 :
            return element.strftime('%a %H:%M:%S')
        else :
            return element.strftime('%d %b %H:%M:%S')

    def get_since_date(self, element):
        """
        Permet d'obtenir le temps écoulé entre maintenant (datetime.now())
        et le temps contenu dans la variable de temps indiquée.

        @param element: nom de l'élément de la classe à utiliser pour le calcul.
        @type element: C{unicode}
        @return: Le temps écoulé depuis la date demandée, ex: "4d 8h 15'".
        @rtype: C{unicode}
        """

        date = datetime.now() - getattr(self, element)
        minutes = divmod(date.seconds, 60)[0]
        hours, minutes = divmod(minutes, 60)
        return "%dd %dh %d'" % (date.days , hours , minutes)

