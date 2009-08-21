# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4: 
"""Modèle pour la table EventHistory"""
from __future__ import absolute_import
from sqlalchemy.orm import mapper
from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.types import Integer, String, Text, DateTime

from sqlalchemy.databases.mysql import MSEnum
from datetime import datetime
from .vigilo_bdd_config import bdd_basename, metadata

# Generation par SQLAutoCode

event_history =  Table(
    bdd_basename + 'event_history', metadata,
    Column(u'idhistory', Integer(), primary_key=True, nullable=False, 
        autoincrement=True),
    Column(u'type_action',
        MSEnum('Nagios update state', 'Acknowlegement change state',
            'New occurence', 'User comment', 'Ticket change', 'Oncall',
            'Forced state'),
        primary_key=False, nullable=False),
    Column(u'idevent', Integer(),
        ForeignKey(
            bdd_basename +'events.idevent'
        ), index=True, primary_key=False, nullable=False),
    Column(u'value',
        String(length=255, convert_unicode=True, assert_unicode=None),
        primary_key=False),
    Column(u'text',
        Text(length=None, convert_unicode=True, assert_unicode=None),
        primary_key=False),
    Column(u'timestamp', DateTime(timezone=False), default=datetime.now(),
        primary_key=False),
    Column(u'username',
        String(length=255, convert_unicode=True, assert_unicode=None),
        primary_key=False),
    mysql_engine='InnoDB',
    mysql_charset='utf8'
)

# Classe a mapper

class EventHistory(object):
    """
    Classe liée avec la table associée
    """
    def __init__(self, type_action, idevent, value='', text='', username=''):
        
        """
        Fonction d'initialisation, permet de faire un INSERT en une fonction

        @param type_action: Le type d'action effectué, peut être 'Nagios update state',
                            'Acknowlegement change state', 'New occurence', 'User comment', 'Ticket change',
                            'Oncall' ou 'Forced state'
        @param idevent: Identifiant de l'évènement
        @param value: Nouvelle sévérité
        @param text: Commentaire sur l'action effectuée
        @param username: Nom d'utilisateur de la personne effectuant l'action
        """

        self.type_action = type_action
        self.idevent = idevent 
        self.value = value
        self.text = text
        self.username = username

mapper(EventHistory, event_history)
