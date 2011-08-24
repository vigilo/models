# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
# Copyright (C) 2006-2011 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

"""Modèle pour la table Event"""
from babel.dates import format_datetime
from sqlalchemy import Column
from sqlalchemy.orm import synonym, relation, aliased
from sqlalchemy.types import Text, DateTime, Integer

from datetime import datetime

from vigilo.models.session import DeclarativeBase, DBSession, ForeignKey
from vigilo.models.tables.statename import StateName
from vigilo.models.tables.supitem import SupItem

__all__ = ('Event', )


class Event(DeclarativeBase, object):
    """
    Événement brut ou correle.

    @ivar idevent: Identifiant de l'événement, tel que fourni par Nagios
        ou genere par le correlateur.
    @ivar timestamp: Date de la dernière occurence de l'événement.
    @ivar idsupitem: Identifiant de l'élément supervisé sur lequel
        porte l'événement.
    @ivar supitem: Instance d'élément supervisé sur laquelle porte
        l'événement.
    @ivar current_state: L'etat courant du service/hote,
        tel que transmis par Nagios, sous forme numérique.
    @ivar initial_state: L'etat initial du service/hote,
        tel que transmis par Nagios, sous forme numérique.
    @ivar peak_state: L'etat du service/hote, tel que transmis
        par Nagios, sous forme numérique.
    @ivar message: Le message transmis par Nagios avec l'événement.

    @note: Cette classe permet de répondre aux exigences suivantes :
        VIGILO_EXIG_VIGILO_BAC_0010.
    """

    __tablename__ = 'event'

    idevent = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True
    )

    timestamp = Column(
        DateTime(timezone=False),
        nullable=False,
    )

    idsupitem = Column(
        Integer,
        ForeignKey(
            SupItem.idsupitem,
            onupdate='CASCADE',
            ondelete='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        index=True,
        nullable=False,
    )

    supitem = relation('SupItem')

    # Informations sur les états de Nagios.
    # Un état peut porter :
    # - sur un hôte (ex: 'UP', 'UNREACHABLE', etc.)
    # - sur un service (ex: 'OK', 'WARNING', 'UNKNOWN', etc.)

    # L'état courant de l'événement.
    # L'état maximal (cf. ci-dessous) est automatiquement
    # mis à jour lorsque l'état courant devient supérieur.
    # L'état initial est automatiquement initialisé.
    _current_state = Column(
        'current_state', Integer,
        ForeignKey(
            StateName.idstatename,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    def _get_current_state(self):
        """Renvoie la valeur textuelle de l'état courant."""
        return self._current_state

    def _set_current_state(self, value):
        """Modifie la valeur textuelle de l'état courant."""
        if self._peak_state is None:
            self._peak_state = value
            self._initial_state = value

        else:
            statename = aliased(StateName)
            statename2 = aliased(StateName)
            higher =    DBSession.query(
                            statename.idstatename,
                            statename2.idstatename,
                        ).filter(statename.idstatename == self._peak_state
                        ).filter(statename2.idstatename == value
                        ).filter(statename2.order > statename.order
                        ).all()

            if higher:
                self._peak_state = value
        self._current_state = value

    current_state = synonym('_current_state',
        descriptor=property(_get_current_state, _set_current_state))

    # Puis, l'état initial.
    # Cet attribut est en lecture seule une fois l'événement créé.
    _initial_state = Column(
        'initial_state', Integer,
        ForeignKey(
            StateName.idstatename,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    def _get_initial_state(self):
        """Renvoie la valeur textuelle de l'état initial."""
        return self._initial_state

    initial_state = synonym('_initial_state',
        descriptor=property(_get_initial_state, None))

    # Et enfin, l'état maximal.
    # Cet attribut est en lecture seule une fois l'événement créé.
    _peak_state = Column(
        'peak_state', Integer,
        ForeignKey(
            StateName.idstatename,
            ondelete='CASCADE',
            onupdate='CASCADE',
            deferrable=True,
            initially='IMMEDIATE',
        ),
        nullable=False,
    )

    def _get_peak_state(self):
        """Renvoie la valeur textuelle de l'état maximal."""
        return self._peak_state

    peak_state = synonym('_peak_state',
        descriptor=property(_get_peak_state, None))

    message = Column(
        Text(length=None, convert_unicode=True, assert_unicode=None),
        nullable=False,
    )


    def __init__(self, **kwargs):
        """
        Initialise un événement brut ou corrélé.
        """
        super(Event, self).__init__(**kwargs)

    def get_date(self, element, locale):
        """
        Permet de convertir une variable de temps en chaîne de caractères.
        Le format utilisé pour représenter la valeur dépend de la locale
        de l'utilisateur.

        @param element: nom de l'élément à convertir de la classe elle même
        @type element: C{unicode}
        @param locale: Locale de l'utilisateur.
        @type locale: C{basestring}
        @return: La date demandée.
        @rtype: C{unicode}
        """
        date = getattr(self, element)
        return format_datetime(date, format='medium', locale=locale)

    def get_since_date(self, element, locale):
        """
        Permet d'obtenir le temps écoulé entre maintenant (datetime.now())
        et le temps contenu dans la variable de temps indiquée.
        Le format utilisé pour représenter la valeur dépend de la locale
        de l'utilisateur.

        @param element: nom de l'élément de la classe à utiliser pour le calcul.
        @type element: C{unicode}
        @param locale: Locale de l'utilisateur.
        @type locale: C{basestring}
        @return: Le temps écoulé depuis la date demandée, ex: "4d 8h 15'".
        @rtype: C{unicode}
        """
        date = datetime.now() - getattr(self, element)
        minutes = divmod(date.seconds, 60)[0]
        hours, minutes = divmod(minutes, 60)
        return "%dd %dh %d'" % (date.days , hours , minutes)
