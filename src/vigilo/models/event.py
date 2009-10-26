# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Event"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import synonym
from sqlalchemy.types import Unicode, UnicodeText, Text, DateTime, Integer

from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase
from .session import DBSession
from .state import state_proxy

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
    @ivar state: L'etat du service/hote, tel que transmis par Nagios.
    @ivar message: Le message transmis par Nagios avec l'evenement.
    """

    __tablename__ = bdd_basename + 'event'

    idevent = Column(
        Unicode(40),
        primary_key=True, nullable=False, #autoincrement=True
    )

    timestamp = Column(DateTime(timezone=False))

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename +'host.name'),
        index=True, nullable=False,
    )

    ip = Column(
        Unicode(40),    # 39 caractères sont requis pour stocker une IPv6
                        # sous forme canonique. On arrondit à 40 caractères.
        index=True, nullable=True,
    )

    servicename = Column(
        Unicode(255),
        ForeignKey(bdd_basename + 'service.name'),
        index=True, nullable=True,
    )

    # Informations sur les états de Nagios.
    # Un état peut porter :
    # - sur un hôte (ex: 'UP', 'UNREACHABLE', etc.)
    # - sur un service (ex: 'OK', 'WARNING', 'UNKNOWN', etc.)
    # Les attributs commençant par "numeric" correspondent à une valeur
    # numérique associée à l'état, tandis que la variante sans le "numeric"
    # correspond à la valeur textuelle.
    # Les transformations nombre <-> texte sont automatiques.

    # L'état courant de l'évènement.
    # L'état maximal (cf. ci-dessous) est automatiquement
    # mis à jour lorsque l'état courant devient supérieur.
    # L'état initial est automatiquement initialisé.
    _numeric_current_state = Column(
        'current_state', Integer,
        autoincrement=False, nullable=False,
    )
    def _get_numeric_state(self):
        return self._numeric_current_state
    def _set_numeric_state(self, value):
        if self._numeric_peak_state is None:
            self._numeric_peak_state = value
            self._numeric_initial_state = value
        elif value > self._numeric_peak_state:
            self._numeric_peak_state = value
        self._numeric_current_state = value
    numeric_current_state = synonym('_numeric_current_state',
        descriptor=property(_get_numeric_state, _set_numeric_state))
    state = state_proxy('numeric_current_state', 'state')

    # Puis, l'état initial.
    # Cet attribut est en lecture seule une fois l'évènement créé.
    _numeric_initial_state = Column(
        'initial_state', Integer,
        autoincrement=False, nullable=False,
    )
    def _get_numeric_initial_state(self):
        return self._numeric_initial_state
    numeric_initial_state = synonym('_numeric_initial_state',
        descriptor=property(_get_numeric_initial_state, None))
    initial_state = state_proxy('numeric_initial_state', 'initial_state')

    # Et enfin, l'état maximal.
    # Cet attribut est en lecture seule une fois l'évènement créé.
    _numeric_peak_state = Column(
        'peak_state', Integer,
        autoincrement=False, nullable=False,
    )
    def _get_numeric_peak_state(self):
        return self._numeric_peak_state
    numeric_peak_state = synonym('_numeric_peak_state',
        descriptor=property(_get_numeric_peak_state, None))
    peak_state = state_proxy('numeric_peak_state', 'peak_state')

    message = Column(
        Text(length=None, convert_unicode=True, assert_unicode=None),
        nullable=False,
    )


    def __init__(self, **kwargs):
        """
        Initialise un évènement brut ou corrélé.
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
        minutes, seconds = divmod(date.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%dd %dh %d'" % (date.days , hours , minutes)

