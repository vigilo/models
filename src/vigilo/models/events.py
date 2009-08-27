# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Events"""
from __future__ import absolute_import

from sqlalchemy import Column, DefaultClause, ForeignKey
from sqlalchemy.types import Integer, UnicodeText, Text, DateTime

from sqlalchemy.databases.mysql import MSEnum, MSBoolean

from datetime import datetime

from .vigilo_bdd_config import bdd_basename, DeclarativeBase


class Events(DeclarativeBase):

    __tablename__ = bdd_basename + 'events'

    idevent = Column(Integer(), primary_key=True, nullable=False,
        autoincrement=True)
    hostname = Column(
        UnicodeText(),
        ForeignKey(bdd_basename +'host.name'),
        index=True, nullable=False)
    servicename = Column(
        UnicodeText(),
        ForeignKey(bdd_basename + 'service.name'),
        index=True)
    severity = Column(Integer(), nullable=False)
    status = Column(MSEnum('None', 'Acknowledged', 'AAClosed'),
        nullable=False,
        server_default=DefaultClause('None', for_update=False))
    active = Column(MSBoolean(), default='True')
    timestamp = Column( DateTime(timezone=False))
    output = Column(
        Text(length=None, convert_unicode=True, assert_unicode=None),
        nullable=False)
    timestamp_active = Column(DateTime(timezone=False))
    trouble_ticket = Column(
        UnicodeText())
    occurence = Column(Integer())
    impact = Column(Integer())
    rawstate = Column(MSEnum('WARNING', 'OK', 'CRITICAL', 'UNKNOWN'))

    def __init__(self, hostname, servicename, server_source = '', severity = 0,
            status = 'None', active = True, timestamp = datetime.now(),
            output = '', event_timestamp = datetime.now(),
            last_check = datetime.now(), recover_output = '',
            timestamp_active = datetime.now(),
            timestamp_cleared=None, trouble_ticket = None,
            occurence = 1):

        self.hostname = hostname
        self.servicename = servicename
        self.server_source = server_source
        self.severity = severity
        self.status = status
        self.active = active
        self.timestamp = timestamp
        self.output = output
        self.event_timestamp = event_timestamp
        self.last_check = last_check
        self.recover_output = recover_output
        self.timestamp_active = timestamp_active
        self.timestamp_cleared = timestamp_cleared
        self.trouble_ticket = trouble_ticket
        self.occurence = occurence

    def get_date(self, element):

        """
        Permet de convertir une variable de temps en la chaîne de caractère :
        jour mois heure:minutes:secondes

        @param element: nom de l'élément à convertir de la classe elle même
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
        et le temps contenu dans la variable de temps indiquée

        @param element: nom de l'élément de la classe elle même à utiliser
                        pour le calcul
        """

        date = datetime.now() - self.__dict__[element]
        minutes, seconds = divmod(date.seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%dd %dh %d'" % (date.days , hours , minutes)


