# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2016 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table CorrEvent"""
from sqlalchemy import Column, DefaultClause, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation

from vigilo.models.utils import DateMixin
from vigilo.models.session import DeclarativeBase
from vigilo.models.tables.secondary_tables import EVENTSAGGREGATE_TABLE
from vigilo.models.tables.event import Event

__all__ = ('CorrEvent', )

class CorrEvent(DeclarativeBase, DateMixin):
    """
    Informations sur un événement corrélé.

    @ivar idcorrevent: Identifiant de l'événement corrélé.
    @ivar idcause: Identifiant de l'événement qui a été identifié
        comme cause principale de l'alerte.
    @ivar cause: Instance de l'événement identifié comme cause de l'alerte.
    @ivar priority: Priorité de l'alerte.
    @ivar trouble_ticket: URL du ticket d'incident se rapportant à
        l'événement corrélé.
    @ivar ack: État de prise en compte de cet événement corrélé.
        Il s'agit d'une des constantes ACK_NONE, ACK_KNOWN ou ACK_CLOSED
        définies ci-dessous.
    @ivar occurrence: Compteur d'occurrences de l'événement corrélé.
        Il est incrémenté par le corrélateur chaque fois que l'état de
        l'événement oscille alors que l'opérateur n'est pas encore intervenu.
    @ivar timestamp_active: Date de dernière ouverture de l'événement.
        Il s'agit de la date de création de l'événement ou de la dernière
        date à laquelle un événement s'est réenclenché, c'est-à-dire,
        est repassé dans un état d'erreur (ie. ni 'OK' ni 'UP') alors que
        l'opérateur avait marqué le problème comme résolu.
    @ivar events: Liste d'instances d'L{Event}s qui sont liés à cette alerte.

    @note: Cette classe permet de répondre aux exigences suivantes :
        VIGILO_EXIG_VIGILO_BAC_0010.
    """

    __tablename__ = 'vigilo_correvent'

    # Constantes pour l'état d'acquittement:
    # - None : événement pas encore pris en compte.
    ACK_NONE = 0
    # - Known : événement pris en compte mais pas acquitté.
    ACK_KNOWN = 1
    # - Closed : événement acquitté (pouvant être fermé).
    ACK_CLOSED = 2

    idcorrevent = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    idcause = Column(
        Integer,
        ForeignKey(
            Event.idevent,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        autoincrement=False,
        nullable=False,
    )

    cause = relation('Event', lazy=True,
        primaryjoin='CorrEvent.idcause == Event.idevent')

    priority = Column(
        Integer,
        nullable=False,
    )

    trouble_ticket = Column(Unicode(255))

    occurrence = Column(Integer)

    timestamp_active = Column(
        DateTime(timezone=False),
        nullable=False,
        index=True,
    )

    ack = Column(
        Integer,
        nullable=False,
        server_default=DefaultClause(str(ACK_NONE), for_update=False),
        index=True,
    )

    events = relation('Event', lazy=True,
        secondary=EVENTSAGGREGATE_TABLE)

    def __init__(self, **kwargs):
        """
        Initialise un événement corrélé.
        """
        super(CorrEvent, self).__init__(**kwargs)

