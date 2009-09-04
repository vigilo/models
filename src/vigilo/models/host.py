# -*- coding: utf-8 -*-
# vim:set expandtab tabstop=4 shiftwidth=4:
"""Modèle pour la table Host"""
from __future__ import absolute_import

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import Integer, Unicode, UnicodeText
from sqlalchemy.orm import relation
from sqlalchemy.ext.associationproxy import association_proxy

from .vigilo_bdd_config import bdd_basename, DeclarativeBase, metadata

__all__ = ('Host', )

class Host(DeclarativeBase):
    __tablename__ = bdd_basename + 'host'

    name = Column(
        Unicode(255),
        index=True,primary_key=True, nullable=False,
        info={'rum': {'field': 'Text'}})

    checkhostcmd = Column(
        UnicodeText(),
        nullable=False)

    community = Column(
        Unicode(255),
        nullable=False)

    fqhn = Column(
        Unicode(255),
        nullable=False)

    hosttpl = Column(
        Unicode(255),
        nullable=False)

    mainip = Column(
        Unicode(15),
        nullable=False)

    port = Column(Integer(), nullable=False)

    snmpoidsperpdu = Column(Integer())

    snmpversion = Column(UnicodeText())

    groups = association_proxy('host_groups', 'groups')


    def __init__(self, name, checkhostcmd = '', community = '', fqhn = '',
            hosttpl = '', mainip = '', port = 0, snmpoidsperdu = 0,
            snmpversion = ''):
        """Initialise un hôte."""
        self.name = name
        self.checkhostcmd = checkhostcmd
        self.community = community
        self.fqhn = fqhn
        self.hosttpl = hosttpl
        self.mainip = mainip
        self.port = port
        self.snmpoidsperdu = snmpoidsperdu
        self.snmpversion = snmpversion

    def __unicode__(self):
        """
        Formatte un C{Host} pour l'afficher dans les formulaires.

        Le nom de l'hôte est utilisé pour le représenter dans les formulaires.

        @return: Le nom de l'hôte.
        @rtype: C{str}
        """
        return self.name


