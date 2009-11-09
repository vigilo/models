# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table EventsAggregate"""
from __future__ import absolute_import

from sqlalchemy import Column, DefaultClause, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation
from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from vigilo.common.conf import settings
from .event import Event
from .secondary_tables import EVENTS_EVENTSAGGREGATE_TABLE, \
                                EVENTSAGGREGATE_HLS_TABLE

__all__ = ('EventsAggregate', )

class EventsAggregate(DeclarativeBase, object):
    """
    Informations sur un ensemble (agrégat) d'évènements,
    corrélés entre eux.
    
    @ivar idcause: Référence à l'évènement faisant partie de L{Event}
        et identifié comme cause primaire de l'ensemble des évènements
        de l'agrégat.
    @ivar impact: Nombre d'hôtes impactés par l'agrégat.
    @ivar trouble_ticket: URL du ticket d'incident se rapportant à l'agrégat.
    @ivar status: Statut de la prise en compte de cet agrégat.
    @ivar occurrences: Compteur d'occurrences de l'agrégat. Il est incrémenté
        chaque fois que l'état de l'évènement oscille alors que l'opérateur
        n'est pas encore intervenu.
    @ivar timestamp_active: Date de dernière ouverture de l'évènement.
    """

    __tablename__ = bdd_basename + 'eventsaggregate'

    idaggregate = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    idcause = Column(
        Integer,
        ForeignKey(
            bdd_basename + 'event.idevent',
            ondelete='CASCADE', onupdate='CASCADE',
        ),
        autoincrement=False,
        nullable=False,
    )

    impact = Column(Integer)

    priority = Column(
        Integer,
        default=settings.get('UNKNOWN_PRIORITY_VALUE', 1),
    )

    trouble_ticket = Column(Unicode(255))

    # État d'acquittement: None, Acknowleged ou AAClosed
    # (Acknowleged And Closed).
    status = Column(Unicode(16),
        nullable=False,
        server_default=DefaultClause('None', for_update=False))

    occurrence = Column(Integer)

    timestamp_active = Column(
        DateTime(timezone=False),
        nullable=False,
    )

    events = relation('Event', lazy='dynamic',
        secondary=EVENTS_EVENTSAGGREGATE_TABLE)

    cause = relation('Event',
        primaryjoin=idcause == Event.idevent, lazy='dynamic')

    high_level_services = relation('Service',
        lazy='dynamic',
        secondary=EVENTSAGGREGATE_HLS_TABLE)


    def __init__(self, **kwargs):
        """
        Initialise un agrégat d'évènements.
        """
        super(EventsAggregate, self).__init__(**kwargs)

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


