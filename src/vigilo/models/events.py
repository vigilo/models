# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Events"""
from __future__ import absolute_import

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Unicode, UnicodeText, Text, DateTime

from sqlalchemy.databases.mysql import MSBoolean

from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase


class Events(DeclarativeBase, object):
    """
    Evènement brut ou corrélé.

    @ivar idevent: Identifiant de l'évènement, tel que fourni par Nagios
        ou généré par le corrélateur.
    @ivar timestamp: Date de ??? XXX à quoi sert ce champ ?
    @ivar hostname: Identifiant de l'hôte concerné par l'évènement.
    @ivar servicename: Identifiant du service concerné par l'évènement.
        Vaut None si l'évènement concerne directement l'hôte.
    @ivar active: ??? XXX à quoi sert ce champ ?
    @ivar state: L'état du service/hôte, tel que transmis par Nagios.
    @ivar message: Le message transmis par Nagios avec l'évènement.
    """

    __tablename__ = bdd_basename + 'events'

    idevent = Column(
        Unicode(255),
        primary_key=True,
        nullable=False)

    # XXX à quoi correspond cette date ???
    timestamp = Column(DateTime(timezone=False))

    hostname = Column(
        Unicode(255),
        ForeignKey(bdd_basename +'host.name'),
        index=True, nullable=False)

    ip = Column(
        Unicode(15),
        index=True, nullable=True)

    servicename = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + 'service.name'),
        index=True, nullable=True)

    active = Column(MSBoolean(), default='True', nullable=False)

    state = Column(Unicode(16))

    message = Column(
        Text(length=None, convert_unicode=True, assert_unicode=None),
        nullable=False)


    def __init__(self, **kwargs):
        """
        Initialise un évènement brut ou corrélé.
        """
        # On empêche la création d'un évènement dans lequel les champs
        # obligatoires ne seraient pas renseignés.
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

