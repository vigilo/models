# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table EventsAggregate"""
from __future__ import absolute_import

from sqlalchemy import Column, DefaultClause, ForeignKey, Table
from sqlalchemy.types import Integer, Unicode, DateTime
from sqlalchemy.orm import relation
from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata
from .event import Event

__all__ = ('EventsAggregate', )

EVENTS_EVENTSAGGREGATE_TABLE = Table(
    bdd_basename + 'eventsaggregates2events', metadata,
    Column('idevent', Unicode(255), ForeignKey(
                bdd_basename + 'event.idevent',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True),
    Column('idaggregate', Integer, ForeignKey(
                bdd_basename + 'eventsaggregate.idaggregate',
                onupdate="CASCADE", ondelete="CASCADE"),
            primary_key=True)
)


class EventsAggregate(DeclarativeBase, object):
    """
    Informations sur un ensemble (aggrégat) d'évènements,
    corrélés entre eux.
    
    @ivar idcause: Référence à l'évènement faisant partie de L{Event}
        et identifié comme cause primaire de l'ensemble des évènements
        de l'agrégat.
    @ivar impact: Nombre d'hôtes impactés par l'agrégat.
    @ivar severity: Gravité du problème.
    @ivar trouble_ticket: URL du ticket d'incident se rapportant à l'agrégat.
    @ivar status: Statut de la prise en compte de cet agrégat.
    @ivar occurrences: Compteur d'occurrences de l'agrégat. Il est incrémenté
        chaque fois que l'état de l'évènement oscille alors que l'opérateur
        n'est pas encore intervenu.
    @ivar timestamp_active: Date de la dernière occurence de l'évènement ou
        de sa dernière modification.
    """

    __tablename__ = bdd_basename + 'eventsaggregate'

    idaggregate = Column(
        Integer,
        primary_key=True, autoincrement=True)

    idcause = Column(
        Unicode(255),
        ForeignKey(bdd_basename + 'event.idevent'))

    impact = Column(Integer)

    severity = Column(Integer)

    trouble_ticket = Column(Unicode(255))
    
    status = Column(Unicode(16),
        nullable=False,
        server_default=DefaultClause('None', for_update=False))

    occurrences = Column(Integer)

    timestamp_active = Column(DateTime(timezone=False))

    events = relation('Event', lazy='dynamic',
        secondary=EVENTS_EVENTSAGGREGATE_TABLE)

    cause = relation('Event',
        primaryjoin=idcause == Event.idevent)


    def __init__(self, **kwargs):
        """
        Initialise un agrégat d'évènements.
        """
        # Empêche la création d'un agrégat lorsque tous les champs
        # obligatoires ne sont pas remplis.
        DeclarativeBase.__init__(self, **kwargs)

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
        minutes, seconds = divmod(date.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%dd %dh %d'" % (date.days , hours , minutes)


