# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Event"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym, relation, aliased
from sqlalchemy.types import Unicode, Text, DateTime, Integer

from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .statename import StateName
from .session import DBSession

__all__ = ('Event', )


class Event(DeclarativeBase, object):
    """
    Evenement brut ou correle.

    @ivar idevent: Identifiant de l'evenement, tel que fourni par Nagios
        ou genere par le correlateur.
    @ivar timestamp: Date de la derniere occurence de l'evenement.
    @ivar hostname: Identifiant de l'hote concerne par l'evenement.
    @ivar servicename: Identifiant du service concerne par l'evenement.
        Vaut None si l'evenement concerne directement l'hote.
    @ivar current_state: L'etat courant du service/hote,
        tel que transmis par Nagios, sous forme numérique.
    @ivar initial_state: L'etat initial du service/hote,
        tel que transmis par Nagios, sous forme numérique.
    @ivar peak_state: L'etat du service/hote, tel que transmis
        par Nagios, sous forme numérique.
    @ivar message: Le message transmis par Nagios avec l'evenement.
    """

    __tablename__ = bdd_basename + 'event'

    idevent = Column(
        Integer,
        primary_key=True, nullable=False, autoincrement=True
    )

    timestamp = Column(DateTime(timezone=False))

    _idservice = Column(
        'idservice', Integer,
        ForeignKey(
            bdd_basename + 'service.idservice',
            onupdate='CASCADE', ondelete='CASCADE',
        ),
        nullable=False,
    )

    service = relation('Service')

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
            bdd_basename + 'statename.idstatename',
            ondelete='CASCADE', onupdate='CASCADE',
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
            bdd_basename + 'statename.idstatename',
            ondelete='CASCADE', onupdate='CASCADE',
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
            bdd_basename + 'statename.idstatename',
            ondelete='CASCADE', onupdate='CASCADE',
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

    def get_date(self, element):
        """
        Permet de convertir une variable de temps en la chaîne de caractère :
        jour mois heure:minutes:secondes

        @param element: nom de l'élément à convertir de la classe elle même
        @type element: C{unicode}
        @return: La date demandée.
        @rtype: C{unicode}
        """

        element = self.__dict__[element]
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

        date = datetime.now() - self.__dict__[element]
        minutes = divmod(date.seconds, 60)[0]
        hours, minutes = divmod(minutes, 60)
        return "%dd %dh %d'" % (date.days , hours , minutes)

